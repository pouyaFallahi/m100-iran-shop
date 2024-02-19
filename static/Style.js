function navbarChange(url) {
    const aHome = document.getElementById('aHome');
    const aProduct = document.getElementById('aProduct')
    const aCategory = document.getElementById('aCategory')

    if (url === 'http://127.0.0.1:8000/' || url === 'http://localhost:8000/') {
        aHome.classList.add("active");
        aProduct.classList.remove("active");
        aCategory.classList.remove("active");
    } else if (url === 'http://127.0.0.1:8000/product/' || url === 'http://localhost:8000/product/') {
        aHome.classList.remove("active");
        aProduct.classList.add("active");
        aCategory.classList.remove("active");
    } else if (url === 'http://127.0.0.1:8000/product/.*/' || url === 'http://localhost:8000/product/') {
        aHome.classList.remove("active");
        aProduct.classList.add("active");
        aCategory.classList.remove("active");
    } else if (url === 'http://127.0.0.1:8000/category/.*/') {
        aHome.classList.remove("active");
        aProduct.classList.remove("active");
        aCategory.classList.add("active");
    }
}