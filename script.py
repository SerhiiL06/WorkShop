from users.models import User
from orders.models import Order

import random


for _ in range(4, 50):
    num = random.randint(1, 50)
    user = User.objects.get(id=num)
    order = Order.objects.create(customer=user, category=random.randint(1, 4))
