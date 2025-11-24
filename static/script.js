    document.getElementById('carForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = {
            brand: document.getElementById('brand').value,
            year: parseInt(document.getElementById('year').value),
            km_driven: parseInt(document.getElementById('km_driven').value),
            fuel_type: document.getElementById('fuel_type').value,
            transmission: document.getElementById('transmission').value,
            owner: document.getElementById('owner').value
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(formData)
            });

            const data = await response.json(); 

            if (data.error) { 
                alert('Error: ' + data.error);
            } else {
                const resultDiv = document.getElementById('result');
                document.getElementById('priceCategory').textContent = `₹${data.predicted_price.toLocaleString('en-IN')}`;
                document.getElementById('resultDescription').textContent = 'Predicted price based on your car details.';
                resultDiv.style.display = 'block';
                resultDiv.scrollIntoView({ behavior: 'smooth' });
            }
        } catch (error) {
            alert('Error connecting to server: ' + error.message); 
        }
    });
