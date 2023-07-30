<script>

        const quantityInputs = document.querySelectorAll('.quantity-input');
        quantityInputs.forEach(input => {
            input.addEventListener('change', function() {
                const basketId = this.dataset.basketId;
                const quantity = this.value;
                updateBasketQuantity(basketId, quantity);
            });
        });


        function updateBasketQuantity(basketId, quantity) {
            const url = "{% url 'products:basket_update_quantity' %}";
            const data = {
                basketId: basketId,
                quantity: quantity
            };

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                // Обновление количества товара в соответствующем элементе на странице
                const quantityElement = document.querySelector(`[data-basket-id="${basketId}"]`);
                quantityElement.value = quantity;
                // Обновление суммы в соответствующем элементе на странице
                const sumElement = quantityElement.parentNode.parentNode.nextElementSibling.querySelector('.col-lg-4');
                sumElement.textContent = data.updatedSum;
                // Обновление общей суммы
                const totalSumElement = document.querySelector('.card-footer .float-right');
                totalSumElement.textContent = data.totalSum;
            }
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
        }
    </script>