function resultsFunc() 
{

    var upload = document.getElementById('upload');

    function onFile() {
        var me = this,
            file = upload.files[0],
            name = file.toString().replace(/\.[^/.]+$/, '');
            var upload_btn = document.getElementById("upload-btn");
            var error = document.getElementById("error-text");

        if (file.type === 'image/png' ||
            file.type === 'image/jpeg'||
            file.type ==='image/jpg') {
            if (file.size < (3000 * 1024)) {
                upload.parentNode.className = 'area uploading';
                upload_btn.style.display = "block";
                if (error.innerHTML != "")
                {
                    error.innerHTML = "";
                }
            } else {
                window.alert('File size is too large, please ensure you are uploading a file of less than 3MB');
            }
        } else {
            window.alert('File type ' + file.type + ' not supported');
        }
    }


    upload.addEventListener('change', function (e) {
        onFile();
    }, false);

}

window.onload = resultsFunc;

