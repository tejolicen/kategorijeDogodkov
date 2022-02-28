<?php
    session_start();
    $action = $_REQUEST["action"];
    if ($action == "predict") {
        predict();
    }
    if ($action == "template_text") {
        templateText();
    }
    function predict() {    
        $search = $_REQUEST["s"];
        $api_url = $_REQUEST["api"];
        // $url = 'https://kategorije-dogodkov.herokuapp.com/predict';

        // use key 'http' even if you send the request to https://...
        $options = array(
            'http' => array(
                'header'  => "Content-type: text/plain\r\n",
                'method'  => 'POST',
                'content' => $search
            )
        );
        $context  = stream_context_create($options);
        $result = file_get_contents($api_url, false, $context);
        if ($result === FALSE) { /* Handle error */ }
        
        echo json_encode($result);
    }
    
    function templateText() {
        echo "GORSKI TEK | ODDIH V NARAVI | ŠPORTNI DAN
        - Registracije so že odprte! -
        Premierna izvedba teka Hrastnik Trail se bo odvila v soboto, 15. maja 2021, na eni izmed idiličnih zasavskih lokacij na sončni planini Kal. ☀🌲🌳
        V objemu narave, zasavskih gozdov, lepih razgledov na okoliške hribe ter doline, se bo lahko prav vsak ljubitelj narave in rekreacije preizkusil v gorskem teku. 🏃‍♀🏃‍♂
        
        Na voljo sta dve trasi:
        👉 1. Si povprečni rekreativec? Potem je trasa TURISTIČNIH 6 zate popolna!
        👉 2. Si tekač in si želiš večjega izziva? Potem je zate trasa RAZGLEDNIH 12.
        Več informacij o trasah in zemljevid:
        📌 https://dogodki.mch.si/#!/trasi
        ✅ Registracija vključuje: majico prve izvedbe teka Hrastnik Trail, topel obrok (mesni/vegi) in sponzorsko darilno vrečko.
        ❗ VELJA SAMO OB SPLETNI PRIJAVI ❗
        ✅ REGISTRIRAJ SE ZDAJ:
        https://dogodki.mch.si/#!/registracija
        
        👉 ŠPORTNI DAN ZA CELO DRUŽINO
        Trasa Turističnih 6 je primerna za celotno družino, zato smo se odločili, da za vse družine pripravimo paket, za popoln športni dan v osrčju narave. Za registracijo dveh staršev in otrok (mlajših od vključno 17 let), boste skupaj z majico Hrastnik Trail in toplim obrokom odšteli le 49,90 EUR. Pogoj za družinsko registracijo je isti stalni naslov na osebnih dokumentih.
        ✅ REGISTRACIJA DRUŽINE:
        https://dogodki.mch.si/#!/za-druzine
        
        👉 PROGRAM GORSKEGA TEKA
        08:00-09:30 Registracija tekačev
        09:30-09:40 Sestanek s tekači
        09:40-09:55 Skupinsko ogrevanje
        10:00-12:00 Štart in tek Razglednih 12
        10:30-13:30 Štart in tek Turističnih 6
        14:00-15:00 Podelitev nagrad in priznanj
        
        📌 LOKACIJA
        Google maps:
        https://goo.gl/maps/jss6GGkxqt1WJxh89
        Navigacija vas lahko vodi do prizorišča preko več poti, vendar niso vse prevozne.
        Na prizorišče lahko pridete samo preko asfaltirane ceste skozi Hrastnik ali Dol pri Hrastniku.
        
        👉 POMEMBNO
        Predvideni športni dogodek se bo izvedel z upoštevanjem vseh priporočili in navodil NIJZ ter ostalih pristojnih institucij. V primeru nezmožnosti izvedbe teka zaradi epidemioloških razmer in ukrepov, je predviden nadomestni termin 25. 9. 2021.";
    }
?>
