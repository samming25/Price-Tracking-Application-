document.getElementById("product-form").addEventListener("submit", function (e) {
    e.preventDefault();

    var name = document.getElementById("product-name").value;
    var url = document.getElementById("product-url").value;
    var price = document.getElementById("product-price").value;

    if (name === "" || url === "" || price === "") {
        alert("All fields are required!");
    } else {
        // Add code here to send form data to a server or to track the product
        alert("Product has been added to tracking list!");
    }
});
