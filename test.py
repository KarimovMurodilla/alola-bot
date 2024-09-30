"""
Result should be:

Заказ - #1234
Наименование товара: Sumka 6095
Цвет и количество:
• Oq - 2
• Qora - 1
Общее количество: 3
Общая сумма: 500000
"""

all_data = [
    {
        "order_id": "d1135hhd-tgw652-hdyy6286d-86hhsf6202",
        "products": [
            {
                "parent_id": "7hsgyyr-uhsgahbd-83hs7h-y2sbhye",
                "name": "Sumka 6095",
                "amount": 500000,
                "colors": [
                    {
                        "product_id": "34d12342-1762535-jhg727-bdy3y32",
                        "color": "oq",
                        "count": 2
                    },
                    {
                        "product_id": "8366273-1762535-jhg727-bdy3y32",
                        "color": "qora",
                        "count": 1
                    }
                ]
            }
        ]
    }
]

result = "Заказ - #1234\n\n"

for product in all_data[0]['products']:
    name = f"Наименование товара: {product['name']}\n"
    amount = f"Общая сумма: {product['amount']}\n"
    colors = "".join([f"• {data['color']} - {data['count']}\n" for data in product['colors']])
    product_count = sum([data['count'] for data in product['colors']])

    result += name
    result += amount
    result += f"Цвет и количество:\n{colors}"
    result += f"Общее количество: {product_count}\n"
    result += f"Общая сумма: {amount}\n\n"

print(result)
