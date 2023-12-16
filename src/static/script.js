function filterOnChange(id) {
    let path = window.location.href.split('?')[0]

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const newValue = document.getElementById(id).value;

    if (newValue != "") urlParams.set(id, newValue);
    else urlParams.delete(id);

    if (id == "limit")
        urlParams.delete("p");

    window.location.replace(path + "?" + urlParams.toString());
}

function paginationOnClick(id) {
    e = document.getElementById(id);
    page = Number(e.getAttribute("p"));

    let path = window.location.href.split('?')[0]

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    urlParams.set("p", page);

    window.location.replace(path + "?" + urlParams.toString());
}

function orderChangeStatus(id, status) {
    const formdata = new FormData();
    formdata.append("order_status", status);

    const requestOptions = {
        method: 'PUT',
        body: formdata,
        redirect: 'follow'
    };

    fetch(id, requestOptions)
        .catch(error => console.log('error', error));
    window.location.replace(id)
}
