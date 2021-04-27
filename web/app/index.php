<html>

<head>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>

</head>

<body>
    <div class="content">
        <div class="btn" onclick="onPotrdi()">Potrdi</div>
    </div>
    <script>

        function onPotrdi() {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                if (this.readyState != 4) return;

                if (this.status == 200) {
                    var data = JSON.parse(this.responseText);
                    console.log(data);
                    // we get the returned data
                }

                // end of state change: it can be after some time (async)
            };
            xhr.open("POST", "request.php?action=predict&s=" + "burek burek burek", true);
            xhr.send("burek");
        }
    </script>
</body>

</html>