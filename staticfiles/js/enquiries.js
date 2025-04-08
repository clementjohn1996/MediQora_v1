document.addEventListener("DOMContentLoaded", function () {
    fetchCountries();

    document.getElementById("id_country").addEventListener("change", function() {
        fetchStates(this.value);
    });

    document.getElementById("id_state").addEventListener("change", function() {
        fetchCities(this.value);
    });

    function fetchCountries() {
        fetch("https://restcountries.com/v3.1/all")
            .then(response => response.json())
            .then(data => {
                let countrySelect = document.getElementById("id_country");
                countrySelect.innerHTML = '<option value="">Select Country</option>';
                data.forEach(country => {
                    countrySelect.innerHTML += `<option value="${country.name.common}">${country.name.common}</option>`;
                });
            })
            .catch(error => console.error("Error fetching countries:", error));
    }


});

document.addEventListener("DOMContentLoaded", function () {
    let today = new Date().toISOString().split("T")[0];
    let dateField = document.getElementById("id_enquiry_date");

    dateField.value = today; // Set default date to today
    dateField.setAttribute("max", today); // Prevent future dates
});