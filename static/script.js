document.querySelector('#downloadBtn').addEventListener('click', function(){
    html2canvas(document.querySelector("#capture"), {
        allowTaint: true,
        useCORS: true,
        ignoreElements: (element) => element.id === 'downloadBtn',
        }).then(canvas=> {
    const downloadLink = document.createElement("a");
    downloadLink.href=canvas.toDataURL("image/png");
    downloadLink.download = "screenshot.png"
    // document.body.appendChild(canvas);
    downloadLink.click()
})
})



