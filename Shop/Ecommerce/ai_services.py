from google import genai
from google.genai import types
from django.conf import settings
from Ecommerce.models import Product, CartItem
from django.db.models import Q
import json
import time

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def get_ai_stylist_recommendation(user_prompt: str, user=None) -> str:
    """
    AI Personal Stylist for Bookly bookstore.
    """

    def search_catalog(keywords: str, max_price: float | None = None) -> str:
        """
        Search the store catalog for books matching keywords.
        Optionally filter by maximum price.

        Args:
            keywords: Search terms (book title, author, genre, etc.)
            max_price: Optional maximum price filter
        """
        print(f"\n[search_catalog] keywords='{keywords}', max_price={max_price}")

        try:
            qs = Product.objects.all()

            if max_price is not None:
                qs = qs.filter(product_price__lte=max_price)

            matched = qs.filter(
                Q(product_name__icontains=keywords) |
                Q(product_desc__icontains=keywords)
            ).distinct()[:8]

            print(f"[search_catalog] Found {matched.count()} products")

            if not matched.exists():
                # Fallback - return some books so AI can still reply usefully
                fallback = Product.objects.all()[:5]
                results = []
                for item in fallback:
                    results.append({
                        "id": item.id,
                        "name": item.product_name,
                        "price": float(item.product_price),
                        "description": (item.product_desc or "")[:140],
                    })
                return json.dumps({
                    "status": "no_exact_match",
                    "message": f"No exact match for '{keywords}'. Showing some available books instead.",
                    "items": results
                })

            results = []
            for item in matched:
                results.append({
                    "id": item.id,
                    "name": item.product_name,
                    "price": float(item.product_price),
                    "description": (item.product_desc or "")[:140],
                })

            return json.dumps({"status": "found", "items": results})

        except Exception as e:
            print(f"[search_catalog] ERROR: {e}")
            return json.dumps({
                "status": "error",
                "message": str(e),
                "items": []
            })

    def add_bundle_to_cart(product_ids: list[int]) -> str:
        """
        Add products to the current user's cart using their IDs.
        Only call this after the user confirms they want the items.

        Args:
            product_ids: List of product IDs from search_catalog
        """
        print(f"\n[add_bundle_to_cart] product_ids={product_ids}")

        if user is None or not getattr(user, "is_authenticated", False):
            return "User is not logged in. Please ask the user to log in first before adding items to cart."

        added_items = []

        for pid in product_ids:
            try:
                product = Product.objects.get(id=pid)

                cart_item, created = CartItem.objects.get_or_create(
                    user=user,
                    product=product,
                    defaults={"quantity": 1}
                )

                if not created:
                    cart_item.quantity += 1
                    cart_item.save()

                added_items.append(product.product_name)

            except Product.DoesNotExist:
                continue
            except Exception as e:
                print(f"[add_bundle_to_cart] Error on product {pid}: {e}")
                continue

        if added_items:
            return f"Success! Added {len(added_items)} item(s) to your cart: {', '.join(added_items)}"

        return "Could not add the items. They may no longer be available."

    system_instruction = """
You are a friendly and expert personal shopping assistant for Bookly, an online bookstore.

Rules you must follow:
1. Always call search_catalog first to find real books.
2. Never invent book names, IDs, or prices. Only use data returned by search_catalog.
3. When the user asks to add something to cart, first search, show them the book, then call add_bundle_to_cart only after confirmation or clear intent.
4. Be warm, helpful and concise.
"""

    try:
        chat = client.chats.create(
            model="gemini-3.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[search_catalog, add_bundle_to_cart],
                temperature=0.5,
            ),
        )

        # Retry logic for temporary 503 errors
        for attempt in range(3):
            try:
                response = chat.send_message(user_prompt)
                return response.text or "Sorry, I couldn't generate a response."
            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    if attempt < 2:
                        time.sleep(2 * (attempt + 1))
                        continue
                raise e

    except Exception as e:
        error_msg = str(e)
        print(f"[AI Stylist Error] {error_msg}")

        if "503" in error_msg or "UNAVAILABLE" in error_msg:
            return "The AI is experiencing high demand right now. Please try again in a moment."
        if "getaddrinfo failed" in error_msg:
            return "Sorry, I can't reach the AI service. Please check your internet connection."

        return f"Sorry, something went wrong. ({error_msg})"























# # ai_services.py
# from google import genai
# from google.genai import types
# from django.conf import settings
# from Ecommerce.models import Product, CartItem
# from django.db.models import Q
# import json

# client = genai.Client(api_key=settings.GEMINI_API_KEY)


# def get_ai_stylist_recommendation(user_prompt: str, user=None) -> str:
#     """
#     Main entry point for the AI Personal Stylist.
#     Uses Gemini with automatic function calling to search catalog
#     and optionally add items to the user's cart.
#     """

#     def search_catalog(keywords: str, max_price: float | None = None) -> str:
#         """
#         Search the store catalog for products matching keywords.
#         Optionally filter by maximum price.

#         Args:
#             keywords: Search terms (book title, author, genre, etc.)
#             max_price: Optional maximum price filter

#         Returns:
#             JSON string with matching products or empty results.
#         """
#         qs = Product.objects.filter(product_is_active=True)

#         if max_price is not None:
#             qs = qs.filter(product_price__lte=max_price)

#         matched = qs.filter(
#             Q(product_name__icontains=keywords) |
#             Q(product_description__icontains=keywords)
#         ).distinct()[:8]

#         if not matched.exists():
#             return json.dumps({"status": "no_results", "items": []})

#         results = []
#         for item in matched:
#             results.append({
#                 "id": item.id,
#                 "name": item.product_name,
#                 "price": float(item.product_price),
#                 "description": (item.product_description or "")[:150],
#             })

#         return json.dumps({"status": "found", "items": results})

#     def add_bundle_to_cart(product_ids: list[int]) -> str:
#         """
#         Add one or more products to the current user's cart by their IDs.
#         Only call this after the user has confirmed they want the items.

#         Args:
#             product_ids: List of product IDs returned earlier by search_catalog

#         Returns:
#             Success or failure message.
#         """
#         if user is None or not user.is_authenticated:
#             return "User is not logged in. Please ask them to log in before adding items to cart."

#         added_items = []
#         for pid in product_ids:
#             try:
#                 product = Product.objects.get(id=pid, product_is_active=True)
#                 cart_item, created = CartItem.objects.get_or_create(
#                     user=user,
#                     product=product,
#                     defaults={"quantity": 1},
#                 )
#                 if not created:
#                     cart_item.quantity += 1
#                     cart_item.save()
#                 added_items.append(product.product_name)
#             except Product.DoesNotExist:
#                 continue

#         if added_items:
#             return f"Success! Added {len(added_items)} item(s) to cart: {', '.join(added_items)}"
#         return "Failed to add items. Products may be unavailable or IDs were invalid."

#     system_instruction = """
# You are an expert personal shopping stylist for Bookly, an online bookstore.
# Your goal is to understand the customer's occasion, taste, and budget,
# then recommend real products from our catalog.

# Strict Rules:
# 1. ALWAYS call search_catalog first to discover real products.
# 2. NEVER invent product names, IDs, or prices. Only use what search_catalog returns.
# 3. Stay strictly within the user's budget when one is given.
# 4. When recommending a bundle, clearly list each book with name, price, and why it fits.
# 5. Only call add_bundle_to_cart after the user explicitly confirms they want to buy / add the items.
# 6. Be friendly, concise, and helpful. Use a warm, literary tone.
# """

#     try:
#         chat = client.chats.create(
#             model="gemini-3.5-flash-lite",          # current stable fast model
#             config=types.GenerateContentConfig(
#                 system_instruction=system_instruction,
#                 tools=[search_catalog, add_bundle_to_cart],
#                 temperature=0.6,
#             ),
#         )

#         response = chat.send_message(user_prompt)
#         return response.text or "Sorry, I couldn't generate a response. Please try again."

#     except Exception as e:
#         print(f"[AI Stylist Error] {e}")
#         return f"Sorry, something went wrong while talking to the stylist. ({str(e)})"































# from google import genai
# from google.genai import types # type: ignore
# from django.conf import settings
# from Ecommerce.models import Product, CartItem
# import json

# client = genai.Client(api_key=settings.GEMINI_API_KEY)

# def get_ai_stylist_recommendation(user_prompt: str, chat_history: list = None, user=None) -> dict:

#     def search_catalog(keywords: str, max_price: float = None) -> str:
#         """
#         Search available products in the store by keyword and optional maximum price.
#         """
#         qs = Product.objects.filter(product_is_active=True)
        


#         # Search in name or description
#         matched = qs.filter(product_name_icontains=keywords) | qs.filter(product_description_icontains=keywords)
#         matched = matched.distinct()[:6]

#         if not matched.exists():
#             return json.dumps({"status": "no_results", "items": []})

#         results = []
#         for item in matched:
#             results.append({
#                 "id": item.id,
#                 "name": item.product_name,
#                 "price": float(item.product_price),
#                 "description": item.product_description[:120]
#             })

#         return json.dumps({"status": "found", "items": results})

#     def add_bundle_to_cart(product_ids : list[int]):
#         added_items = []
#         print(product_ids)
#         for pid in product_ids:
#             try:
#                 product = CartItem.objects.get(id=pid, product_is_active=True)
#                 cart_item, created = CartItem.objects.get_or_create(
#                     user=user,
#                     product=product,
#                     defaults={'quantity': 1}
#                 )
#                 if not created:
#                     cart_item.quantity += 1
#                     cart_item.save()
#                     added_items.append(product.product_name)

#             except Product.DoesNotExist:
#                 continue
            
#         if added_items:
#             return f"Success! Added {len(added_items)} items to cart: {', '.join(added_items)}"
           
#         return "Failed to add items to cart. Items might be out of stock."
    
#     system_instruction = """
#     You are an expert personal shopping stylist for an e-commerce platform.
#     Your goal is to understand the customer's occasion, taste, and budget, 
#     and curate a complete matching bundle using products from our store catalog.
    
#     Rules:
#     1. call search_catalog to check for the item/product.
#     2. NEVER invent fake product IDs or products that aren't returned by search_catalog.
#     3. Stay strictly within the user's budget if one is stated.
#     4. Add all the products in the currespondings users cart using this method add_bundle_to_cart
#     5. Response back the users with a success message if product already added to cart.
#     """

#     # Hand the search_catalog function directly to Gemini
#     chat = client.chats.create(
#         model='gemini-3.6-flash',
#         config=types.GenerateContentConfig(
#             system_instruction=system_instruction,
#             tools=[search_catalog, add_bundle_to_cart],
#             temperature=0.7,
#         )
#     )

#     response = chat.send_message(user_prompt)
#     return response.text