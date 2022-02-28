<html>

<head>

    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="spinner.css">
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        label {
            font-weight: bold;
        }
        .content {
            display: flex;
            flex-direction: column; 
            max-width: 44rem;
            padding: 2rem;
            width: 100%;
        }

        #inputTextToPredict {
            height: 20rem;
        }

        .buttons {
            display: flex;
            align-items: center;
            justify-content: flex-end;
        }
    </style>
</head>

<body>
    <div class="content">
        <div class="forma">
            <form>
                <div class="form-group">
                    <label for="inputApiUrl">API URL</label>
                    <input type="text" class="form-control" id="inputApiUrl" value="https://kategorije-dogodkov.herokuapp.com/predict" disabled>
                </div>
                <div class="form-group">
                    <label for="inputTextToPredict">Opis dogodka</label>
                    <textarea class="form-control" id="inputTextToPredict"></textarea>
                </div>
                <div class="buttons">
                    <div class="loader_container">
                        <div class="loader" id="loader"></div>
                    </div>
                    <button id="btnPotrdi" class="btn btn-primary" onclick="onPotrdi(); return false;">Potrdi</button>
                </div>

            </form>
        </div>
        <div class="results">
            <div class="form-group">
                <label for="outputNapoved">Napoved</label>
                <div id="outputNapoved"></div>
            </div>
        </div>
    </div>
    <script>
        function onPotrdi() {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (this.readyState != 4) return;

                if (this.status == 200) {
                    var data = JSON.parse(JSON.parse(this.response));
                    console.log(data["prediction"]);
                    $('#outputNapoved').text(data["prediction"]);
                }
                $('#loader').removeClass('loader-active');
                $('#btnPotrdi').removeAttr('disabled');

                // end of state change: it can be after some time (async)
            };
            var value = $('#inputTextToPredict').val();
            var apiUrl = $('#inputApiUrl').val();
            xhr.open("GET", "request.php?action=predict&api=" + apiUrl + "&s=" + value, true);
            xhr.send();
            $('#loader').addClass('loader-active');
            $('#btnPotrdi').attr('disabled', true);
        }

        function onAppStart() {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (this.readyState != 4) return;

                if (this.status == 200) {
                    $('#inputTextToPredict').val(this.responseText);
                }

                // end of state change: it can be after some time (async)
            };
            xhr.open("GET", "request.php?action=template_text", true);
            xhr.send();
        }
        $( document ).ready(function() {
            onAppStart();
        });
        
    </script>
</body>

</html>