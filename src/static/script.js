function filterOnChange(id) {
    let path = window.location.href.split('?')[0]

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const newValue = document.getElementById(id).value;

    if (newValue != "") urlParams.set(id, newValue);
    else urlParams.delete(id);

    window.location.replace(path + "?" + urlParams.toString());
}
