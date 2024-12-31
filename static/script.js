document.querySelector('#downloadBtn').addEventListener('click', function(){
    html2canvas(document.querySelector("#capture"), {
        allowTaint: true,
        ignoreElements: (element) => element.id === 'downloadBtn'
    }).then(canvas=> {
    document.body.appendChild(canvas);
    console.log("complete");
})
})



