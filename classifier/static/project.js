function resultsFunc() 
{

    var upload = document.getElementById('upload');

    function onFile() {
        var me = this,
            file = upload.files[0],
            name = file.toString().replace(/\.[^/.]+$/, '');
            uploaded = false;

        if (file.type === 'image/png' ||
            file.type === 'image/jpeg'||
            file.type ==='image/jpg') {
            if (file.size < (3000 * 1024)) {
                upload.parentNode.className = 'area uploading';
                uploaded = true;
            } else {
                uploaded = false;
                window.alert('File size is too large, please ensure you are uploading a file of less than 3MB');
            }
        } else {
            uploaded = false;
            window.alert('File type ' + file.type + ' not supported');
        }
    }

    upload.addEventListener('dragenter', function (e) {
        upload.parentNode.className = 'area dragging';
    }, false);

    upload.addEventListener('dragleave', function (e) {
        upload.parentNode.className = 'area';
    }, false);

    upload.addEventListener('dragdrop', function (e) {
        onFile();
    }, false);

    upload.addEventListener('change', function (e) {
        onFile();
    }, false);

    console.log("Getting File")

  function sendFile ()
  {
      var upload = document.getElementById('upload');
      var url_link = $("#url-link").attr("data-url");
      console.log(url_link);
      console.log(upload);
      var file = upload.files[0]
      console.log(file);
      console.log("Sending File")
      $.ajax({
          url: url_link,
          type: 'POST',
          processData: false,
          contentType: false,
          data: file.serialize(),

          success: function (data, status,) {
              //success code
          },
          error: function (jqxhr, status, msg) {
              //error code
          }
      });
  }

//   var submit_file = document.getElementById('file-submit');
//   submit_file.addEventListener("click", sendFile);

}

window.onload = resultsFunc;

