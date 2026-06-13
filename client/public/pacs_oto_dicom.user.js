// ==UserScript==
// @name         PACS BESK OTO DICOM (557 hasta)
// @namespace    nurcan.tez
// @version      1.6
// @description  PROHIMS Studies - TURBO mod: hizli enumeration, azaltilmis bekleme sureleri
// @match        http://pacs.besk.local/ImageServer/Pages/Studies/*
// @match        https://pacs.besk.local/ImageServer/Pages/Studies/*
// @run-at       document-idle
// @grant        none
// ==/UserScript==

(function () {
  'use strict';

  function rTimeout(fn, ms) { setTimeout(fn, ms); }

  // ============ HASTA LISTESI (557 hasta, 18-65, K+E) ============
  var HASTALAR = [["28784376364","ACET_MELEK",31,"K",306],["10135128494","AGA_SADET",62,"K",873],["27004922848","AGUS_EMINE",60,"K",289],["27154479032","AKA_SEVGI",23,"K",289],["15527911944","AKALTUN_BERFIN",20,"K",1736],["63547463424","AKBEYAZ_BARAA",31,"K",321],["28337313426","AKGUL_FERIHA",62,"K",330],["14906364036","AKPINAR_ILAY",21,"K",310],["10255312100","AKSOY_SUREYYA",58,"K",297],["28549120966","AKYOL_MUJGAN",43,"K",329],["10534178694","ALPAY_KUBRA_NUR",19,"K",289],["10534178694","ALPAY_KUBRA_NUR",19,"K",289],["21979834328","ALTAN_YASANLAR_BUSE",32,"K",317],["31652112674","ALTAYHAN_SIRVAN",24,"K",282],["23378663592","ALTUN_AKKADIN",47,"K",270],["32854426880","ALTUNTOP_RABIA",45,"K",301],["23174364358","ARIK_VURAL_NURMELEK",30,"K",285],["15298124956","ARIKAN_NUR",30,"K",306],["10156541272","ARPACI_NESRIN",47,"K",313],["23069518330","ARSLAN_SEMSI",64,"K",297],["16372033140","ASLAN_NEBAHAT",62,"K",269],["16672506160","ATAKAN_ASLI",28,"K",289],["25769612042","ATUG_GOKSU",44,"K",313],["23723540714","AVCI_FATMA",47,"K",318],["31862450122","AVSAR_ASLIHAN",24,"K",293],["24349603876","AYDEMIR_ZELIHA",47,"K",309],["12475046650","AYDOGDU_AYSEL",61,"K",285],["12658214470","AYGUN_DILARA",27,"K",277],["10087332802","BAGATUR_IREM",21,"K",301],["19019726948","BALOGLU_MIMOZA_CISIL",28,"K",290],["99773013492","BARAKAT_ALIA",56,"K",322],["99773013492","BARAKAT_ALIA",56,"K",345],["43726708232","BARUG_NIHAN",41,"K",313],["19547835754","BASAR_GAMZE",40,"K",297],["19381020958","BAYINDIR_EMINE",61,"K",289],["47578607194","BILCANOGLU_ZEYNEP",39,"K",289],["12037178638","BILGIN_HULYA",47,"K",1490],["37517261372","BILICAN_HATICE",65,"K",301],["12304259220","BILYAN_ROZERIN",25,"K",302],["15466062448","BOLAT_HICAZIYE",51,"K",302],["38291212154","BOSTAN_SENAY",40,"K",826],["58885090272","BOZDAG_HALENUR",26,"K",282],["30805800420","BOZKURT_FADIME",30,"K",297],["35822155720","BOZKURT_ALKAYA_DERYA",32,"K",309],["37751091070","BULUT_BELGIN",57,"K",281],["24524009882","BULUT_DONDU",54,"K",782],["11848244822","BULUT_SELMA",52,"K",293],["15745154338","BUYUKATAK_MEHPARE_AYSUN",46,"K",310],["28373299654","BUYUKKOPRU_SIMGE",22,"K",5275],["31265069822","CAGLAYAN_SENAY",53,"K",1797],["10876166892","CAGLAYAN_SEVVAL_YAGMUR",18,"K",2155],["34231568800","CALISKAN_AYLIN",39,"K",305],["16447974248","CELIK_AYSER",65,"K",277],["33865988718","CELIK_ELIF",36,"K",297],["26356188278","CELIK_HACER",53,"K",333],["50506512194","CELIK_MUNEVVER",55,"K",281],["15427076552","CELIK_SALIHA",28,"K",309],["18115993490","CELIKTAS_ZERRIN_ZEYNEP",54,"K",270],["10751346210","CELLIK_SEVVAL",20,"K",703],["38473092994","CERRAHOGLU_FATMA",57,"K",301],["11349010896","CEVIK_KUBRA",35,"K",357],["40343143798","CEYLAN_ESRA",36,"K",293],["27245375106","CICEK_NURAN",52,"K",322],["23867000860","CIFTCI_ALIME",45,"K",289],["70606090828","CIFTCI_SEMIHA",43,"K",293],["15229078150","CINAR_ASLIHAN",32,"K",309],["50923052174","COLAK_MELIKE",34,"K",289],["10247943336","COP_GULCAN",54,"K",3275],["12004066548","COPUR_NIHAYET",52,"K",317],["31609365924","DAL_MELEK",39,"K",309],["36983054570","DALGIC_NURAN",33,"K",2731],["14548890368","DANACI_GULSEM",65,"K",321],["26507706092","DEGRI_TUVANA",49,"K",342],["24746209374","DEMIR_FATMA",30,"K",301],["26659237178","DEMIR_HACER",64,"K",289],["11461573132","DEMIR_SERA",33,"K",290],["26408385938","DEMIR_SEYHAN",46,"K",262],["63082274158","DEMIR_SONGUL",39,"K",3150],["27439455706","DEMIR_ZEHRA_BETUL",27,"K",306],["61102370224","DEMIREL_GULSEREN",64,"K",2963],["41257346350","DINCER_SEVIL",58,"K",330],["10420174458","DOGAN_FATMA",61,"K",357],["50296550406","DONMEZ_GULSAN",21,"K",341],["33094312230","DONSAK_ZOHRE",47,"K",298],["68509168058","DUMAN_YETER",64,"K",293],["53059581310","DURAK_AYNUR",53,"K",310],["57028535410","DURAK_MUHSINE",44,"K",254],["42289178810","DURMAZ_TOKSOY_BILGE",46,"K",329],["10069564528","ELDEM_SEVCAN_NUR",21,"K",317],["32282112416","ELIBOL_HANDESU",24,"K",569],["14905159138","ELMAS_AYHAN",64,"K",298],["11081671904","ERGIN_SEYDA",19,"K",285],["39311122170","ERGUN_SEBILE",26,"K",342],["15050274622","ERGUN_ZEHRA",63,"K",321],["29140563268","ERSOY_OZLEM",52,"K",318],["20897793106","ERTEGI_AYSEL",62,"K",305],["17188044092","ERTUC_FATMA",59,"K",269],["14417439766","ESER_MURUVET",58,"K",365],["33380056244","EVET_RABIA",58,"K",277],["27899317118","FIRAT_PINAR",44,"K",294],["33335264694","GENCER_DENIZ",25,"K",282],["10274215888","GEYIK_EZGI_BENGI",30,"K",333],["25388415208","GOKALP_AYSE",60,"K",313],["34834505158","GOKCE_AYSEL",56,"K",382],["24664566122","GOZACIK_GULCIHAN",46,"K",3041],["10001050850","GUL_MERYEM",25,"K",294],["18146882480","GULEC_SEDA",36,"K",318],["34426892918","GULISIK_HUDANUR",22,"K",294],["41782338196","GULKAN_AYNIL",28,"K",306],["11296267138","GUNES_SUDE",20,"K",2120],["11152532752","GUNGOR_KADRIYE",51,"K",326],["11726130674","GUR_SERAP",65,"K",306],["72166040398","HALICI_CAFIYE",57,"K",309],["21529125524","HAMAMCI_NERGIZ",34,"K",301],["14801480466","HATIPOGLU_BILGE",35,"K",314],["14098108012","HICYILMAZ_SAZIYE",57,"K",561],["99173557916","HORODETSKA_LIUDMYLA",30,"K",2176],["13762109324","ICOZ_BUSRA_ASLI",22,"K",278],["47449344098","INAM_EKIN_DOGA",25,"K",306],["13375023598","ISIK_SEVGI",60,"K",289],["10432275228","IVGEN_ZEYNEP",48,"K",310],["99421332654","JEIRANASHVILI_NANA",57,"K",356],["47965921216","KABA_SEDA_NUR",27,"K",270],["10697590692","KABAK_HATICE_NUR",20,"K",341],["16435013744","KACAR_FATMA",51,"K",1523],["15340008708","KAHRAMAN_SINE",36,"K",742],["57358163772","KALE_GULPERI",65,"K",301],["23786464156","KANAT_REYHAN",60,"K",305],["18731794976","KARA_BIRSEN",37,"K",309],["17792660862","KARAARSLAN_IZEM",29,"K",358],["68293179230","KARADAG_ZEYNEP",54,"K",297],["10351850698","KARADENIZ_SERPIL",65,"K",281],["36439173602","KARADUT_MELIHA",47,"K",294],["17842047834","KARAHAN_SILA",22,"K",289],["12127173734","KARAHANCI_MUJDE",47,"K",318],["25129537824","KARAKOC_NEJLA",39,"K",302],["19298857470","KARATAY_BELKIZ",23,"K",298],["34372238136","KARGI_HULYA",44,"K",290],["40174076784","KARGIN_BEDIHA",56,"K",297],["38149893498","KARTAL_SANIYE",44,"K",329],["10274228444","KASKA_ARZU",22,"K",346],["13768151136","KAVAK_NAZLI_GUL",25,"K",1362],["12475173370","KAYABASI_MENEKSE",30,"K",1411],["10039425408","KAYACAN_GULHAN",46,"K",294],["14081979346","KAYHAN_SULE_ZEYNEP",35,"K",261],["37033288600","KAYMAZ_ESRA",27,"K",282],["37939110418","KAYNAK_DONDU",61,"K",330],["11761274470","KENAR_SAFIYE",50,"K",297],["11029082496","KESER_FATMA",57,"K",289],["23941617014","KESKIN_DURNA",61,"K",290],["14770125276","KILIC_ARZU",51,"K",289],["12355026352","KILIC_CANSEVER",54,"K",330],["12355026352","KILIC_CANSEVER",54,"K",607],["28774450142","KILICARSLAN_GULAY",52,"K",302],["11326211568","KILINCARSLAN_TULAY",54,"K",366],["15314658328","KINALI_DUZEYLI_GULSUM",37,"K",333],["43573391656","KIR_ARDIC_SERIFE",47,"K",3114],["23543280388","KIRIKISLA_ALABAY_ESRA",37,"K",289],["20513355824","KIZILIRMAK_DURHANIM",52,"K",294],["42463702480","KIZILKAYA_MEDINE",63,"K",322],["12166413464","KIZILTUNCDEN_KARADENIZ_BEYZANUR",28,"K",325],["11164281464","KOC_NEZIHA",62,"K",770],["60574233730","KOCAK_GULUMSER",53,"K",301],["28367304104","KODAK_ELIFE",51,"K",356],["29596401534","KOKVER_HATICE",46,"K",289],["23246510362","KONCA_GUFER",47,"K",298],["10660112838","KORKMAZ_DONMUS",40,"K",321],["54718495788","KORKMAZ_HATICE",45,"K",285],["29354009798","KOSANOGLU_NURHAYAT",62,"K",289],["23182979360","KOSK_HATICE",25,"K",2458],["19397861026","KOTEK_ADALET",61,"K",317],["23890619244","KOYLU_ZULBIYE",53,"K",298],["20845693298","KUCUK_GUL",35,"K",309],["35323991308","KUDUS_HURIYE",45,"K",314],["51481063930","KULABER_EMINE",24,"K",334],["37025205172","KURUMLU_SEDA",35,"K",302],["22747621898","LEYLEK_AYSENUR",30,"K",305],["42241853762","LOK_MEYREM",58,"K",273],["13567075374","LOUKIANOVA_SVETLANA",49,"K",705],["43132333776","MANDAL_AYSE",54,"K",270],["13741094122","MESGEN_OZDEMIR_GONCA",38,"K",325],["20644105046","MISIR_GONUL",51,"K",299],["36622372034","MORKOC_GULSUN",44,"K",322],["99447575370","NADIRLI_ASIMAN",22,"K",278],["22891211792","NAMLI_FATMA",64,"K",321],["99729021762","NASER_NAZIYA_JASIM_AHMED",47,"K",337],["12394203172","ONCUL_EDA",32,"K",305],["66709016612","ONER_AYTEN",58,"K",1891],["35615022284","OVSEME_HAYRIYE",42,"K",301],["14794011142","OZ_DILEK",48,"K",2020],["65914054600","OZCAN_BUSE",27,"K",5669],["11207373712","OZCELIK_IREM",20,"K",858],["10761081880","OZDEMIR_SALIHA_GUL",20,"K",273],["17464777058","OZDENIZ_MUKADDES_FATMA",36,"K",352],["39244469854","OZDIL_OZDE_NUR",27,"K",2297],["68833151634","OZIPEK_GULER_DONDU",32,"K",309],["36586145828","OZKARA_YELIZ",47,"K",290],["12070156686","OZLESEN_MURSIDE",46,"K",313],["15529005894","OZTEKIN_FEHRUNISA",63,"K",813],["13480064882","OZTURK_HATICE",62,"K",309],["53458706604","OZTURK_PINAR",43,"K",301],["14258063694","OZTURK_TULAY",64,"K",334],["15211251660","PAKSOZER_SEMA",63,"K",285],["57532367132","PAMUK_AYSE",56,"K",290],["45550708396","PEKTAS_PINAR",41,"K",305],["12691048360","POLAT_DILAN",28,"K",290],["99196339278","SAKVARELIDZE_NARGIZA",62,"K",285],["30532929722","SAL_BERNA",58,"K",350],["37840138396","SALMAN_AFIRE",56,"K",281],["24728608478","SAMANTIR_AYPERI",57,"K",305],["32257235560","SARI_MINE_SELIN",34,"K",297],["16597124432","SARITAS_FEYZA_NUR",25,"K",329],["26567238908","SAYDAN_BETUL",34,"K",825],["61984410520","SECEN_FATMA",51,"K",290],["10360024028","SENER_MURSIDE",23,"K",325],["38242858202","SEZER_ZEYNEP",39,"K",723],["44914101576","SILAHSOR_REFIKA",25,"K",326],["11443064092","SINAN_DILBER",62,"K",519],["10351322164","SOKEN_MEHTAP",35,"K",306],["33055309132","SOLUGAN_SILA",21,"K",289],["63052343310","SOYLU_FATMA",46,"K",297],["99223483516","SULAKVELIDZE_NANA",65,"K",367],["17047068306","SULUNOGLU_SEVGI",46,"K",338],["15070025358","SUMEN_ECEM",23,"K",298],["11455591326","SUR_SEMIHAN",53,"K",325],["14239656860","TABAKCI_KUDRET",55,"K",290],["14239656860","TABAKCI_KUDRET",55,"K",278],["25910389052","TASDEMIR_NEBAHAT",52,"K",293],["16579115342","TEBER_AYBUKE",23,"K",281],["19060583866","TELEK_CANAN",42,"K",317],["12758826122","TEMIZ_NECLA",63,"K",844],["69826117606","TETIK_HANIFE",50,"K",369],["12088274518","TIMUCIN_KEVSER",61,"K",309],["26225375136","TOP_FUNDA",61,"K",771],["56761627246","TOPAL_DEFNE_ASYA",34,"K",285],["37960133462","TOPCU_HATICE",53,"K",329],["98284223086","TORKAMANI_FAEZEH",27,"K",281],["16807016458","TUMTURK_NESE",42,"K",278],["58036429906","TUNC_MAHI_MEHRI",65,"K",1470],["39637250892","TURGUT_SALTANAT",48,"K",281],["61504035622","TURKMEN_GULER",54,"K",301],["12958204348","ULUCAN_ELIFNUR",27,"K",297],["24178967576","ULUS_AYSE_DILSAH",22,"K",803],["27373610032","YALCIN_GUNES_GUNAY",57,"K",317],["11953268836","YALMANCIOGLU_GULSAH",33,"K",265],["10825320832","YARDIM_NISA",20,"K",294],["10942227366","YARDIMCI_SELMA",44,"K",325],["58702212344","YAYLAK_ZULEYHA",60,"K",310],["11704252732","YESILYURT_ZEYNEP",20,"K",349],["27007939096","YILDIRIM_NURETTIN",56,"K",293],["15658722624","YILDIRIM_SUKRAN",51,"K",309],["10165490264","YILDIZ_GORKEM",43,"K",297],["32203944850","YILDIZ_TUBA",29,"K",322],["14983604926","YILMAZ_CANSEV",39,"K",289],["10579185770","YILMAZ_DURU",19,"K",309],["34039901144","YILMAZ_FUNDA",31,"K",3155],["11189185778","YILMAZ_GULSEN",64,"K",269],["10735324814","YILMAZ_ILAYDA",22,"K",278],["14767010028","YILMAZ_MUALLA",62,"K",294],["10768407812","YILMAZ_OYKU",19,"K",350],["27319672940","YILMAZ_SENGUL",54,"K",269],["36154406818","YILMAZ_SERMIN",34,"K",338],["62617366580","YILMAZ_ZEYNEP",36,"K",269],["31454073388","YURTTAS_OLGU",30,"K",286],["11390615422","ACIKGOZOGLU_RECEP",46,"E",310],["37019184384","AKCA_OSMAN",60,"E",302],["21146338154","AKMESE_ALI_OSMAN",60,"E",317],["52411614420","AKPINAR_SERVET",61,"E",326],["11166026216","AKSEHIR_KEREM_SABRI",19,"E",829],["23998573196","AKTAS_ISA",30,"E",302],["10355237938","AKTAS_YUSUF_TAHA",19,"E",309],["65320372312","AKTASOGLU_EFE_NAIM",18,"E",297],["38486207750","AKTURK_ABDULAZIZ",37,"E",314],["28411641490","AKTURK_ABDULLAH",53,"E",309],["99054849154","AL-MADHOUN_AHMED_M_R",30,"E",301],["40015045986","ALEMDAR_MEHMET",34,"E",3555],["99499437824","ALIYEV_NIJAT",21,"E",293],["14791351494","ALTUNTAS_RAMAZAN",63,"E",326],["21926633776","ALUC_UGUR",33,"E",305],["16666347830","ARSLAN_BARIS_BERZAN",22,"E",318],["22948877636","ARSLAN_OMER",36,"E",310],["54820624304","ARSLAN_SERKAN",46,"E",309],["12394255584","ARSLAN_VEYSEL",19,"E",321],["11175176582","ARTUC_BERKE_ARBEN",23,"E",334],["60553335202","ASCI_BAHRI",30,"E",1989],["15901446628","ASLAN_IRFAN",55,"E",357],["68422226798","ASLAN_ZIYETTIN",58,"E",298],["46315468388","ATAKUL_ISIK",51,"E",313],["11528810286","ATILGAN_MUHARREM",21,"E",812],["38338255366","AYAR_YAKUP",62,"E",333],["39382066434","AYDUGAN_SERKAN",49,"E",325],["29734084636","AYKAN_ILKER",45,"E",305],["99587593432","AZEEZ_MOHAMMED_AHMED_AZEEZ",51,"E",1725],["39823058424","BABACANOGLU_GAZI",28,"E",305],["10972592342","BABAN_EMRAH",27,"E",1140],["59707444112","BABAT_EMRAH",24,"E",1792],["14349003004","BADEMCI_TEVFIK",63,"E",322],["36869210410","BAKIR_HACI_YUSUF",64,"E",294],["48910584784","BALTA_RECEP",39,"E",322],["20753802096","BARDAKCI_MUHAMMED",27,"E",322],["42217007328","BARUG_RASIT",52,"E",334],["27004701832","BASARIR_SEZEN",50,"E",310],["43910061150","BAYDIN_MUSTAFA_VAKIF",64,"E",310],["11413179726","BAYRAKTAR_SADIK",27,"E",346],["26579151196","BAYTOK_AHMET_BURAK",30,"E",310],["65527266896","BELEN_RAMAZAN",34,"E",278],["29180279952","BERKTAS_MEHMET_DOGAN",55,"E",338],["10171257318","BESKAYA_FATIHCAN",19,"E",1437],["55585506942","BOYREK_EREN",25,"E",1858],["10565682788","BOZDEMIR_ALI_MIRAC",18,"E",2065],["18206844250","BULUT_BEKIR",39,"E",2146],["10582173412","BULUT_IBRAHIM",42,"E",298],["12778005842","CAKIR_ABDURRAHMAN",46,"E",3281],["15406063320","CAKIR_TUNAHAN",22,"E",1433],["15010737600","CAKIRALP_HUSEYIN",41,"E",333],["22888616876","CAKMAK_ISRAFIL",56,"E",277],["58378556940","CAKMAK_NEVZAT",49,"E",310],["10340058258","CAKMAK_ONUR",19,"E",313],["19423020304","CALI_ILHAMI",63,"E",4359],["20051449566","CANPOLAT_HASAN",25,"E",309],["43642799048","CATKILI_AHMET",46,"E",1992],["16684099070","CELIK_BULENT",60,"E",345],["25217236042","CENGIZ_ABDULLAH",54,"E",558],["12145250202","CENGIZ_ADEM",63,"E",357],["12694012702","CETIN_MUHAMMED_SECKIN",36,"E",314],["49552405284","CETINKAYA_OMER_MALIK",58,"E",314],["16424153758","CINGOZ_MURAT",62,"E",321],["52840505368","COPOGLU_ALTUG",39,"E",329],["13765004466","CORUK_CEBRAIL",38,"E",313],["10078219884","CULHA_AYTEKIN",50,"E",322],["39172215684","DAG_OGUZHAN_AHMET",39,"E",345],["12517017150","DALGIC_HAKAN",58,"E",341],["14827428084","DEGER_KAZIM",49,"E",318],["26552490328","DEMIR_BULENT",63,"E",301],["51397451814","DEMIRCAKAN_HUSEYIN",61,"E",2763],["12958092938","DEMIRDAS_HAYDAR",53,"E",301],["41722008318","DENIZ_ALI",61,"E",297],["11035900470","DIKICI_RAMAZAN",63,"E",302],["26977057496","DILMAC_MURAT",25,"E",313],["46270543472","DINC_SUAYIP",54,"E",294],["28928238114","DOGAN_ALI",29,"E",342],["27605576716","DOGAN_EKREM",62,"E",294],["10054329958","DOGAN_INANC_ERIM",21,"E",822],["10045145796","DOGAN_MEHMET_KAAN",20,"E",306],["12637040328","DOGAN_VELI",54,"E",325],["31349475174","DORUK_FEYZI",65,"E",305],["13990002138","DUMAN_ILKER",40,"E",357],["47158608818","DUNDAR_ADIL_MURAT",57,"E",329],["11800064864","DURDU_MEHMET",62,"E",341],["12073164992","DURMAZ_MUSTAFA_BILAL",44,"E",579],["52966565352","DURSUN_MEHMET",34,"E",302],["36349484584","ERALDEMIR_SERVER",45,"E",407],["13748986994","ERASLAN_YALCIN",51,"E",317],["10891150982","ERBAS_AHMET",48,"E",326],["11225743498","ERCAN_MUHAMMET_BAHATTIN",61,"E",314],["37325200822","ERCIYAS_SONER",60,"E",346],["10247007472","ERCUMEN_BERAT",19,"E",1416],["35119071030","ERDOGAN_CEMIL",50,"E",282],["27307469064","ERDOGAN_FIRAT_CAN",27,"E",357],["30778354388","ERDUGAN_SEVKET_SEDAT",25,"E",345],["14975277114","ERGUN_MUHAMMET_KEREM",27,"E",301],["10699017340","ERKAN_IBRAHIM",44,"E",1270],["17932309880","ERNUR_MIFTAH_MUZAFFER",63,"E",310],["38345276682","EROL_EFE",18,"E",844],["42157783276","ERSOY_ISMAIL",61,"E",318],["41050248004","ERTURK_SATILMIS",56,"E",317],["13555072132","ESEN_RAMAZAN",46,"E",337],["15664057048","ESEN_UMUT",37,"E",338],["52387447572","ESER_ERHAN",37,"E",295],["13135216406","EVIRGEN_KUBULAY",30,"E",289],["51163134026","EYILI_SAMET",63,"E",1310],["64834153790","FIDAN_MURAT",47,"E",293],["36346151526","FINDIK_ISMAIL",65,"E",301],["57583391438","GENC_KOKSAL",42,"E",306],["10495306570","GEREDELI_SALIH",51,"E",321],["11578268402","GOKCE_NUMAN",41,"E",317],["41912051698","GOKCE_NUSRAT",51,"E",350],["33238623932","GOKTAS_BATUHAN",23,"E",293],["33203142918","GOMBEL_KURSAT",28,"E",326],["62086063720","GORAL_ERMAN",38,"E",305],["68017000710","GUDUK_SERDAR",35,"E",329],["55576550244","GULBAHAR_SEYFI",35,"E",341],["53632569414","GULCAN_BURKAY",31,"E",322],["34843388810","GULDALI_ALI",59,"E",309],["26786083358","GULERYUZ_MURAT",48,"E",314],["43622054860","GULTEKIN_ERBIL",64,"E",309],["17272080388","GUMUS_BILAL",64,"E",289],["33521202110","GUNAY_ALI",52,"E",2013],["46591714940","GUNDOGAR_HAMZA",45,"E",345],["33814437496","GUNER_MUHAMMET_AKIF",39,"E",978],["36112051470","GUNES_BURHAN",49,"E",310],["12712258266","GUNES_MEHMET_EMIN",18,"E",333],["48331407594","HASDEMIR_ERCAN",50,"E",309],["24020104722","HERGUNER_YUKSEL",57,"E",317],["53023564042","HILAL_YUNIS",46,"E",314],["29530721964","IBIS_HILMI",44,"E",1008],["10726179676","ICIK_ENES",19,"E",305],["14594304314","ILHAN_NECATI_VEFA",53,"E",301],["14594304314","ILHAN_NECATI_VEFA",53,"E",325],["15790312806","INAN_NOFEL_HAKAN",49,"E",329],["17936659196","INCE_HAKAN",52,"E",334],["45070903424","IRTEM_CAFER",43,"E",358],["11398302782","ISIK_BATUHAN",26,"E",2388],["29507095838","ISIK_BUNYAMIN",49,"E",361],["11097028266","KABADAYI_BERAT",19,"E",357],["11867930218","KAPUKIRAN_BERK",19,"E",309],["11437057918","KAR_EMRAH",60,"E",354],["10118717714","KARAASLAN_BERAT",22,"E",313],["38458077596","KARABINAR_SATILMIS",64,"E",277],["55612185508","KARABULUT_NIHAT",54,"E",314],["33430760466","KARADAS_ARDA",21,"E",1237],["11998284518","KARADUMAN_EMRE",30,"E",301],["58246096134","KARAKILIC_ORHAN",47,"E",298],["48631407362","KARAKUS_EMIRHAN",29,"E",333],["18832730934","KARATAS_SALIM",60,"E",1395],["33218050956","KARCI_MURAT_FEHMI",62,"E",338],["31868059572","KARCI_SAIT",60,"E",314],["34054240440","KARSAVURANOGLU_ILHAN",60,"E",3197],["11260488392","KART_MUHAMMED",29,"E",848],["99560580800","KASSAB_MOHAMMED_HUSSEIN_JASIM",20,"E",286],["16907235452","KAYA_ABDULMECID_EMRE",21,"E",333],["29426148882","KAYA_CENGIZ",36,"E",313],["37916097046","KAYA_KORAY_HASRET",32,"E",305],["58162481724","KAYA_MEHMET",58,"E",277],["35110208404","KAYA_NESIMI",49,"E",417],["31768901780","KAYA_SAVAS",47,"E",318],["55642399340","KELAV_ARIF",30,"E",325],["14509904158","KELSAKA_SERDAR",63,"E",298],["11212127300","KESIKBASOGLU_AZIZ",28,"E",310],["17629844472","KILINC_OGUZ_KAAN_CAGATAY",41,"E",317],["10759298900","KILINC_SAIM",61,"E",329],["10078206464","KIRCABEL_SINAN",19,"E",321],["49024072266","KISLIOGLU_YASAR_ERGIN",65,"E",317],["10400756834","KIZBUT_ALPARSLAN_TALHA",27,"E",313],["12562047096","KIZIL_YUNUS_EMRE",30,"E",293],["19336332044","KOC_ONUR",33,"E",310],["11191284940","KOCABAY_YUSUF_OGUZHAN",35,"E",1449],["27010513368","KOCAER_ESVET",53,"E",916],["35656897414","KOYUNCU_MUSTAFA",36,"E",305],["12904157964","KULAKSIZ_ILYAS",52,"E",329],["13032079296","KURSUN_NEVZAT",47,"E",5541],["13582015140","MERMER_ENVER",42,"E",326],["44860234236","MISIR_HUSEYIN",53,"E",357],["99780597442","MOUNDOUNGA_MAVOUROULOU_SERAPHIN",22,"E",848],["41132150164","MUS_SERTAC",31,"E",326],["13060035806","NAMALAN_IBRAHIM_OGUZHAN",28,"E",309],["25355372978","OCAK_ATA",36,"E",796],["15175133804","ODABAS_MUSTAFA",57,"E",301],["13877901714","OKATAN_FARUK",60,"E",345],["13948050426","OKUR_SELAHATTIN_FURKAN",27,"E",3465],["13948050426","OKUR_SELAHATTIN_FURKAN",27,"E",321],["12163725614","OLCAY_TARKAN",55,"E",309],["10903850466","ONALAN_MUHAMMED_EMIR",19,"E",774],["36722217594","ONER_EREN",41,"E",329],["13411145246","OPOZ_KADIR",60,"E",318],["18664518908","ORAL_ARIF",48,"E",305],["61006003488","ORMAN_KERIM",40,"E",4364],["50929216532","OZ_HAKKI_OGUZ",18,"E",321],["51946459902","OZCAN_MEHMET_NURI",46,"E",326],["20504594874","OZCAN_OZER",52,"E",337],["14228881464","OZCAN_YILMAZ",49,"E",317],["18635390892","OZDAMAR_RESAT_NART",52,"E",354],["35810342668","OZDEMIR_MUSTAFA",23,"E",302],["33907278784","OZDEMIRCAN_METIN",64,"E",322],["14680990254","OZENK_MEHMET",37,"E",301],["34843239174","OZGUDEN_SEDAT",40,"E",1835],["61126323992","OZGUR_DENIZ_CAGLAR",28,"E",326],["32141107706","OZTURK_ABDULLAH",41,"E",866],["25748005292","PAKEL_AYKIN_BERK",46,"E",305],["57346285370","POLAT_EMRAH",45,"E",317],["62851344856","POLAT_GUVEN",52,"E",365],["11977065466","POLAT_MUSTAFA",58,"E",373],["14832035994","POYRAZ_ALI_IHSAN",61,"E",333],["21796877546","POYRAZ_KENAN",55,"E",594],["10364157142","PUSKULLU_KEREM",19,"E",346],["25598464430","SAGLAM_ARSLAN_BARIS",49,"E",1594],["14555555038","SAHAN_SUNULLAH",64,"E",337],["10969270420","SAHIN_AHMET",61,"E",270],["15466160694","SAHIN_ERDAL",61,"E",342],["70726088378","SAHIN_ERDOGAN",55,"E",289],["19354005074","SAHIN_MEHMET",63,"E",337],["46726931198","SAHIN_MERT_CAN",29,"E",305],["27950234484","SAHIN_SEZER",30,"E",3278],["44437135584","SARIBAS_UGUR",48,"E",301],["11044802550","SARICA_BURAK",28,"E",321],["26602523006","SARIER_DURSUN",51,"E",293],["47818222026","SAYGILI_HALIL",32,"E",305],["40712182410","SAYIN_MURAT",23,"E",585],["17551084472","SEFIL_TAYFUN",31,"E",1428],["18295044586","SENER_FATIH",59,"E",322],["57184451050","SENGUL_TURKUAZ",32,"E",309],["20623269066","SEVINC_MAHMUT",32,"E",305],["39491015248","SEZER_MURAT",54,"E",357],["99545897466","SHIKHLAR_KHALID_GHAEB_SAEED",51,"E",330],["13315027686","SIMSEK_ABDULMUTTALIP",26,"E",301],["14518104914","SIRMACI_MURAT",46,"E",333],["46555786860","SOFTA_AHMET_MUSTAFA",54,"E",318],["11308211524","SONMEZ_MURAT",37,"E",409],["69673128664","SOYLU_HALIL",52,"E",631],["17381131308","SUNER_EMIN",52,"E",878],["32638907840","TABAK_CEVAT",62,"E",317],["14530103568","TANRIYAKUL_KUBILAY",40,"E",297],["21673409068","TANYER_ALTAN",42,"E",318],["18043989664","TAS_HAKAN",26,"E",317],["12490050168","TASKAN_SERKAN",52,"E",2069],["15791984330","TASKIRAN_UNAL",61,"E",302],["25399168216","TASLI_MUSTAFA_RECEP",35,"E",317],["14761085596","TEMIZSOY_UMMET",56,"E",1036],["32521160178","TETIK_ERSOY",53,"E",309],["11356212450","TETIK_UFUK",35,"E",305],["18289073042","TIFTIKCI_OKAN",26,"E",338],["45952476046","TIVER_MEHMET",30,"E",1737],["65320131742","TORE_FEHMI",56,"E",345],["11440089524","TORUM_VOLKAN",29,"E",305],["12544043610","TOSUN_YASIN",42,"E",2153],["14485135966","TUNC_ABDULLAH_FURKAN",18,"E",3390],["12964190192","TUZUN_UMUTCAN",32,"E",632],["40666326700","UCAN_RIZA",41,"E",337],["49690429418","UCAR_ENDER",51,"E",321],["51070335004","ULAS_ISMAIL",37,"E",277],["32749735752","ULUKAN_RECEP",51,"E",318],["16499487390","ULUSOY_YAKUP",63,"E",289],["13369210218","UNAL_ONUR",40,"E",322],["21925506774","UNLU_OGUZCAN",32,"E",1632],["14201349868","URGUN_SERVET",51,"E",301],["10290040310","USTUNDAG_MIRBAY",20,"E",450],["10825160766","UZUN_ABDULLAH",62,"E",362],["35207147470","UZUN_SELAHATTIN",62,"E",321],["99684603218","VORONTSOV_DMYTRO",47,"E",353],["27481665290","VURAL_AHMET",38,"E",306],["14015168624","VURUPALMAZ_HAKAN",35,"E",321],["10483155210","YAGIMLI_HUSEYIN_HAKAN",42,"E",325],["10528318884","YAMAN_CELIL",21,"E",1862],["11074273252","YAMAN_NEBI_CAN",22,"E",334],["19465792092","YANMAZ_MEHMET_EMRE",35,"E",639],["23182157706","YASAR_BEDRAN_MEM",26,"E",293],["45664922794","YAYLAGUL_EBUBEKIR",37,"E",313],["45235687404","YAZAR_MUSTAFA",54,"E",293],["28796080662","YIGIT_YUSUF",21,"E",309],["28376415860","YILDIRIM_ARIF_ENES",28,"E",325],["46828971702","YILDIRIM_MUHAMMED_YASIN",24,"E",1321],["17212013872","YILDIRIM_NIHAT",44,"E",305],["12088124714","YILDIRIM_UBEYDE",23,"E",289],["49444516838","YILDIRIMKAYA_CEMAL",46,"E",358],["32065290478","YILDIZ_ISMAIL",57,"E",353],["10664978416","YILDIZATA_ERCAN",36,"E",309],["34813874930","YILMAZ_CAGRI_CAN",30,"E",310],["18089433916","YILMAZ_HAKAN",51,"E",314],["10402123610","YILMAZ_HASAN",37,"E",334],["17053049122","YILMAZ_KENAN",39,"E",309],["61177305886","YILMAZ_OZKAN",44,"E",337],["14046042528","YILMAZ_UMIT",32,"E",310],["39332046066","YUKSEKDAG_TUGAY",32,"E",345],["52273295218","ZENCIRLI_FATIH",39,"E",321],["43105746336","ZEREN_OGUN",24,"E",381],["17236065628","ZORLU_CAGLAR",40,"E",4221],["43219752520","ZULFIKAR_ONAL",53,"E",341]];
  // Format: [tc, "SOYAD_AD", yas, "K"|"E", kesit_tahmini]


  // ============ AYARLAR ============
  var CONFIG = {
    SEARCH_TIMEOUT_MS: 30000,
    VIEWER_OPEN_TIMEOUT_MS: 20000,
    ZIP_TIMEOUT_MS: 120000,
    BETWEEN_PATIENT_DELAY_MS: 2000,
    // Calismayi secme kurallari (tez icin):
    // - "BT BEYIN" iceren VE "KONTRASTSIZ" iceren
    // - "KONTRASTLI", "DIFUZYON", "ANJIO", "PERFUZYON" iceren atlanir
    // - Tarihi NISAN 2026 olmali
    HEDEF_AY_YIL: ['NISAN 2026', 'NİSAN 2026', 'NIS 2026', 'NİS 2026', '04.2026', '/04/2026', '-04-2026', '2026-04', '2026.04'],
  };

  // ============ DURUM YONETIMI (localStorage - same-origin, viewer ile paylasilir) ============
  var GM = {
    get: function (k, d) {
      try {
        var v = localStorage.getItem(k);
        if (v == null) return d;
        if (v[0] === '{' || v[0] === '[') return JSON.parse(v);
        if (v === 'true') return true;
        if (v === 'false') return false;
        return v;
      } catch (_) { return d; }
    },
    set: function (k, v) {
      try { localStorage.setItem(k, typeof v === 'object' ? JSON.stringify(v) : String(v)); } catch (_) {}
    },
    del: function (k) { try { localStorage.removeItem(k); } catch (_) {} },
  };

  function defaultState() {
    return {
      aktif: false,
      i: 0,
      bitti: [],
      hata: [],
      atlandi: [],
      t0: Date.now(),
      lastTC: '',
    };
  }

  function getCompleted() {
    try { return JSON.parse(localStorage.getItem('COMPLETED_TCS') || '{}'); } catch (_) { return {}; }
  }
  function markCompleted(tc, info) {
    var c = getCompleted();
    c[tc] = info || true;
    try { localStorage.setItem('COMPLETED_TCS', JSON.stringify(c)); } catch (_) {}
  }
  function isCompleted(tc) {
    return !!getCompleted()[tc];
  }

  // ============ LOG ============
  function log(msg, color) {
    var c = color || 'lime';
    console.log('%c[OTO] ' + msg, 'background:#003;color:' + c + ';font-weight:bold;padding:2px 6px;border-radius:3px');
    var el = document.getElementById('oto-log');
    if (el) {
      var line = document.createElement('div');
      line.style.color = c;
      line.style.fontSize = '11px';
      line.style.lineHeight = '1.4';
      line.textContent = '[' + new Date().toLocaleTimeString('tr-TR') + '] ' + msg;
      el.insertBefore(line, el.firstChild);
      while (el.children.length > 30) el.removeChild(el.lastChild);
    }
  }

  // ============ YARDIMCI: BUL ============
  function findInputByLabel(labelText) {
    var labels = document.querySelectorAll('label, td, th, span, div');
    for (var i = 0; i < labels.length; i++) {
      var t = (labels[i].textContent || '').trim().toLowerCase();
      if (t.indexOf(labelText.toLowerCase()) >= 0 && t.length < labelText.length + 5) {
        // Bu label'in yakininda input bul
        var parent = labels[i].closest('tr, td, div, fieldset') || labels[i].parentElement;
        if (!parent) continue;
        var inp = parent.querySelector('input[type=text], input:not([type])');
        if (inp) return inp;
        // Sonraki kardes
        var sib = labels[i].nextElementSibling;
        while (sib) {
          var inp2 = sib.tagName === 'INPUT' ? sib : sib.querySelector && sib.querySelector('input[type=text], input:not([type])');
          if (inp2) return inp2;
          sib = sib.nextElementSibling;
        }
      }
    }
    // Fallback: id veya name'inde gecen
    var key = labelText.toLowerCase().replace(/[^a-z0-9]/g, '');
    var inputs = document.querySelectorAll('input[type=text], input:not([type])');
    for (var j = 0; j < inputs.length; j++) {
      var idn = ((inputs[j].id || '') + (inputs[j].name || '')).toLowerCase();
      if (idn.indexOf(key) >= 0) return inputs[j];
    }
    return null;
  }

  function findButtonByText(texts) {
    if (!Array.isArray(texts)) texts = [texts];
    var buttons = document.querySelectorAll('button, input[type=button], input[type=submit], a');
    for (var i = 0; i < buttons.length; i++) {
      var t = (buttons[i].value || buttons[i].textContent || '').trim();
      for (var k = 0; k < texts.length; k++) {
        if (t.toLowerCase() === texts[k].toLowerCase() || t.toLowerCase().indexOf(texts[k].toLowerCase()) >= 0) {
          if (t.length <= texts[k].length + 5) return buttons[i];
        }
      }
    }
    return null;
  }

  // Tarihte hedef ay/yil var mi kontrol et (NISAN 2026)
  function isHedefTarih(text) {
    var T = (text || '').toUpperCase();
    for (var i = 0; i < CONFIG.HEDEF_AY_YIL.length; i++) {
      if (T.indexOf(CONFIG.HEDEF_AY_YIL[i]) >= 0) return true;
    }
    return false;
  }

  // Calisma satirini sec: SADECE BT BEYIN KONTRASTSIZ + NISAN 2026
  // Disla: KONTRASTLI, DIFUZYON, ANJIO, PERFUZYON, MRG, AYAKTA, AKCIGER, ABDOMEN, BATIN, HIPOFIZ
  function findStudyRow(tc) {
    var rows = document.querySelectorAll('tr');
    var matches = [];
    var anyTC = 0;
    var btKontrastsizSayi = 0;

    for (var i = 0; i < rows.length; i++) {
      var rt = (rows[i].innerText || '').toUpperCase();
      if (rt.indexOf(tc) < 0) continue;
      anyTC++;

      // Olumlu kosullar
      var hasBT = (rt.indexOf('BT BEYIN') >= 0 || rt.indexOf('BT BEYİN') >= 0 || rt.indexOf('BEYIN BT') >= 0 || rt.indexOf('BEYİN BT') >= 0 || rt.indexOf('BT KRANIAL') >= 0 || rt.indexOf('BT CRANIAL') >= 0);
      var isKontrastsiz = (rt.indexOf('KONTRASTSIZ') >= 0 || rt.indexOf('KONTRASTSİZ') >= 0 || rt.indexOf('NON-CONTRAST') >= 0 || rt.indexOf('KONTRASTSIZ.') >= 0);

      // Olumsuz kosullar (disla)
      var isKontrastli = (rt.indexOf('KONTRASTLI') >= 0 || rt.indexOf('KONTRASTLİ') >= 0);
      var isDifuzyon = (rt.indexOf('DIFUZYON') >= 0 || rt.indexOf('DİFÜZYON') >= 0 || rt.indexOf('DIFFUSION') >= 0 || rt.indexOf('DWI') >= 0);
      var isAnjio = (rt.indexOf('ANJIO') >= 0 || rt.indexOf('ANJİO') >= 0 || rt.indexOf('ANGIO') >= 0);
      var isPerfuzyon = (rt.indexOf('PERFUZYON') >= 0 || rt.indexOf('PERFÜZYON') >= 0);
      var isMRG = (rt.indexOf('MRG') >= 0 || rt.indexOf('MR ') >= 0);
      var isOther = (rt.indexOf('AYAKTA') >= 0 || rt.indexOf('AKCIGER') >= 0 || rt.indexOf('AKCİĞER') >= 0 || rt.indexOf('ABDOMEN') >= 0 || rt.indexOf('BATIN') >= 0 || rt.indexOf('HIPOFIZ') >= 0 || rt.indexOf('HİPOFİZ') >= 0);

      if (!hasBT) continue;
      if (!isKontrastsiz) continue;
      if (isKontrastli || isDifuzyon || isAnjio || isPerfuzyon) continue;
      if (isMRG) continue;
      if (isOther) continue;

      btKontrastsizSayi++;

      // Tarih NISAN 2026 mi?
      if (!isHedefTarih(rt)) continue;

      // Kesit sayisi (cok kesitli olani tercih et)
      var cells = rows[i].querySelectorAll('td');
      var maxNum = 0;
      cells.forEach(function (c) { var n = parseInt((c.textContent || '').trim(), 10); if (!isNaN(n) && n > maxNum && n < 50000) maxNum = n; });
      matches.push({ row: rows[i], kesit: maxNum });
    }

    // Hata mesajini ozelletir
    findStudyRow._lastInfo = { anyTC: anyTC, btKontrastsizSayi: btKontrastsizSayi, matches: matches.length };

    if (matches.length === 0) return null;
    matches.sort(function (a, b) { return b.kesit - a.kesit; });
    return matches[0].row;
  }


  // ============ AKIS ============
  var OTO = {
    _busy: false,
    _audioStarted: false,
    baslat: function () {
      if (OTO._busy) { log('Zaten calisiyor, bekleyin...', 'orange'); return; }
      if (!OTO._audioStarted) { keepAliveAudio(); OTO._audioStarted = true; }
      var s = GM.get('STATE', null);
      if (!s || !s.aktif) {
        s = defaultState();
        s.aktif = true;
        GM.set('STATE', s);
        log('BASLATILDI ' + HASTALAR.length + ' hasta', 'lime');
      } else {
        log('Devam ediyor #' + s.i, 'orange');
      }
      OTO._sonraki();
    },
    durdur: function () {
      var s = GM.get('STATE', defaultState());
      s.aktif = false;
      OTO._busy = false;
      GM.set('STATE', s);
      log('DURDURULDU', 'red');
    },
    sifirla: function () {
      GM.del('STATE'); GM.del('OTO_DONE'); GM.set('OTO_AUTO', false);
      log('SIFIRLANDI', 'orange');
      OTO._renderUI();
    },
    durum: function () {
      var s = GM.get('STATE', defaultState());
      console.table({ aktif: s.aktif, indeks: s.i, toplam: HASTALAR.length, bitti: s.bitti.length, hata: s.hata.length, atlandi: s.atlandi.length });
    },
    atla: function () {
      var s = GM.get('STATE', defaultState());
      if (!s.aktif) { log('aktif degil', 'red'); return; }
      var h = HASTALAR[s.i];
      if (h) s.atlandi.push(h[0]);
      s.i++;
      GM.set('STATE', s);
      log('ATLANDI: ' + (h ? h[0] : '?'), 'orange');
      rTimeout(function () { OTO._sonraki(); }, 1000);
    },

    _sonraki: function () {
      OTO._busy = true;
      var s = GM.get('STATE', defaultState());
      if (!s.aktif) { OTO._busy = false; log('Beklemede', 'gray'); return; }
      if (s.i >= HASTALAR.length) {
        s.aktif = false;
        OTO._busy = false;
        GM.set('STATE', s);
        var dk = Math.round((Date.now() - s.t0) / 60000);
        var compCount = Object.keys(getCompleted()).length;
        log('TAMAMLANDI! ' + compCount + ' toplam indirildi, ' + s.hata.length + ' hata, ' + s.atlandi.length + ' atlandi (' + dk + 'dk)', 'lime');
        return;
      }
      var h = HASTALAR[s.i];
      if (isCompleted(h[0])) {
        log('ATLANDI (onceden indirildi): ' + h[1], '#888');
        s.i++;
        GM.set('STATE', s);
        rTimeout(function () { OTO._sonraki(); }, 100);
        return;
      }
      log('### ' + (s.i + 1) + '/' + HASTALAR.length + ' TC=' + h[0] + ' ' + h[1] + ' (' + h[3] + ', ' + h[2] + ' yas)', 'cyan');
      s.lastTC = h[0];
      GM.set('STATE', s);
      OTO._ara(h);
    },

    _ara: function (h) {
      var tcInp = findInputByLabel('Hasta Numarasi') || findInputByLabel('Hasta Numarası') || findInputByLabel('TC');
      if (!tcInp) { return OTO._hata('TC input yok'); }

      var adInp = findInputByLabel('Hasta Adi') || findInputByLabel('Hasta Adı');
      if (adInp) { adInp.value = ''; adInp.dispatchEvent(new Event('input', { bubbles: true })); }

      tcInp.focus();
      tcInp.value = h[0];
      tcInp.dispatchEvent(new Event('input', { bubbles: true }));
      tcInp.dispatchEvent(new Event('change', { bubbles: true }));

      var searchBtn = findButtonByText(['Ara', 'Bul', 'Search']);
      if (!searchBtn) { return OTO._hata('Arama butonu yok'); }
      log('Arama: ' + h[0], 'orange');
      searchBtn.click();

      OTO._sonucBekle(h, 0);
    },

    _sonucBekle: function (h, n) {
      var row = findStudyRow(h[0]);
      if (row) {
        log('BT Beyin Kontrastsiz NISAN 2026 bulundu (' + (n * 1.5).toFixed(1) + 'sn)', 'lime');
        return OTO._ac(h, row);
      }
      // Sonuclar yuklendi mi (en az 2sn bekle ki sayfa AJAX cevabini alsin)
      var info = findStudyRow._lastInfo || { anyTC: 0, btKontrastsizSayi: 0 };
      if (n >= 4 && info.anyTC > 0) {
        // TC icin satirlar var ama hicbiri filtreye uymadi - fail fast
        return OTO._hata(h[0] + ' eslesme yok (TC=' + info.anyTC + ' sat, BT-Kontrastsiz=' + info.btKontrastsizSayi + ', NISAN2026=0)');
      }
      if (n * 1500 >= CONFIG.SEARCH_TIMEOUT_MS) {
        return OTO._hata(h[0] + ' bulunamadi (timeout)');
      }
      rTimeout(function () { OTO._sonucBekle(h, n + 1); }, 1500);
    },

    _ac: function (h, row) {
      // PROHIMS: BT Beyin satirina 3 kere ardarda tiklamak gerekiyor (viewer acmak icin)
      var firstTd = row.querySelector('td') || row;
      localStorage.setItem('OTO_AUTO', '1');
      GM.del('OTO_DONE');

      function fireClick(el) {
        try {
          ['mousedown', 'mouseup', 'click'].forEach(function (typ) {
            el.dispatchEvent(new MouseEvent(typ, { bubbles: true, cancelable: true, view: window, button: 0 }));
          });
        } catch (_) { try { el.click(); } catch (__) {} }
      }

      log('Satira 3x tiklaniyor...', 'orange');
      fireClick(firstTd);
      rTimeout(function () { fireClick(firstTd); }, 350);
      rTimeout(function () {
        fireClick(firstTd);
        try {
          firstTd.dispatchEvent(new MouseEvent('dblclick', { bubbles: true, cancelable: true, view: window, button: 0 }));
        } catch (_) {}
        log('Viewer acilmasi bekleniyor...', 'orange');
        OTO._zipBekle(h, 0);
      }, 700);
    },

    _zipBekle: function (h, n) {
      var d = GM.get('OTO_DONE', null);
      if (d) {
        if (d.ok) {
          var s = GM.get('STATE', defaultState());
          s.bitti.push(h[0] + ':' + d.kesit + 'k:' + d.mb + 'MB');
          s.i++;
          GM.set('STATE', s);
          GM.del('OTO_DONE');
          GM.set('OTO_AUTO', false);
          markCompleted(h[0], d.kesit + 'k_' + d.mb + 'MB');
          log('OK ' + h[0] + ' ' + d.kesit + ' kesit / ' + d.mb + ' MB', 'lime');

          // Istatistik
          var dk = Math.round((Date.now() - s.t0) / 60000);
          var ort = s.bitti.length > 0 ? dk / s.bitti.length : 0;
          var kalan = HASTALAR.length - s.i;
          log('Toplam: ' + s.bitti.length + '/' + HASTALAR.length + '  Hata: ' + s.hata.length + '  Sure: ' + dk + 'dk  Kalan~' + Math.round(kalan * ort) + 'dk', 'cyan');
          rTimeout(function () { OTO._sonraki(); }, CONFIG.BETWEEN_PATIENT_DELAY_MS);
        } else {
          GM.del('OTO_DONE');
          GM.set('OTO_AUTO', false);
          OTO._hata('ZIP hatasi: ' + (d.hata || '?'));
        }
        return;
      }
      var maxSec = (CONFIG.VIEWER_OPEN_TIMEOUT_MS + CONFIG.ZIP_TIMEOUT_MS) / 1000;
      if (n * 2 >= maxSec) {
        GM.set('OTO_AUTO', false);
        return OTO._hata('Viewer/ZIP timeout (' + maxSec + 'sn)');
      }
      rTimeout(function () { OTO._zipBekle(h, n + 1); }, 2000);
    },

    _hata: function (msg) {
      var s = GM.get('STATE', defaultState());
      var h = HASTALAR[s.i];
      log('HATA: ' + msg, 'red');
      if (h) s.hata.push(h[0] + ':' + msg);
      s.i++;
      GM.set('STATE', s);
      rTimeout(function () { OTO._sonraki(); }, CONFIG.BETWEEN_PATIENT_DELAY_MS);
    },

    _renderUI: function () {
      if (document.getElementById('oto-panel')) return;
      var p = document.createElement('div');
      p.id = 'oto-panel';
      p.style.cssText = 'position:fixed;top:10px;right:10px;z-index:2147483647;background:#001a33;color:#fff;padding:10px;border-radius:8px;font:12px Consolas,monospace;box-shadow:0 4px 16px rgba(0,0,0,.6);width:340px;border:2px solid #0af';
      p.innerHTML =
        '<div style="font-weight:bold;color:#0af;margin-bottom:8px;display:flex;justify-content:space-between">OTO DICOM v1.8<span id="oto-count" style="color:#888;font-size:11px"></span></div>' +
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;margin-bottom:8px">' +
        '<button id="oto-btn-start" style="padding:6px;background:#070;color:#fff;border:0;border-radius:4px;cursor:pointer;font-weight:bold">[>] BASLAT</button>' +
        '<button id="oto-btn-stop" style="padding:6px;background:#a00;color:#fff;border:0;border-radius:4px;cursor:pointer;font-weight:bold">[X] DURDUR</button>' +
        '<button id="oto-btn-skip" style="padding:6px;background:#a60;color:#fff;border:0;border-radius:4px;cursor:pointer">[>>] ATLA</button>' +
        '<button id="oto-btn-reset" style="padding:6px;background:#444;color:#fff;border:0;border-radius:4px;cursor:pointer">[O] SIFIRLA</button>' +
        '</div>' +
        '<div id="oto-log" style="max-height:240px;overflow-y:auto;background:#000;padding:6px;border-radius:4px;border:1px solid #234"></div>';
      document.body.appendChild(p);
      document.getElementById('oto-btn-start').onclick = function () { OTO.baslat(); };
      document.getElementById('oto-btn-stop').onclick = function () { OTO.durdur(); };
      document.getElementById('oto-btn-skip').onclick = function () { OTO.atla(); };
      document.getElementById('oto-btn-reset').onclick = function () { if (confirm('Tum ilerleme silinecek, emin misin?')) OTO.sifirla(); };

      setInterval(function () {
        var s = GM.get('STATE', defaultState());
        var compCount = Object.keys(getCompleted()).length;
        var cnt = document.getElementById('oto-count');
        if (cnt) cnt.textContent = s.i + '/' + HASTALAR.length + ' OK:' + compCount + ' ERR:' + s.hata.length;
      }, 1000);
    },
  };

  try { window.OTO = OTO; } catch (_) {}
  try { if (typeof unsafeWindow !== 'undefined') unsafeWindow.OTO = OTO; } catch (_) {}

  function keepAliveAudio() {
    try {
      var ctx = new (window.AudioContext || window.webkitAudioContext)();
      var osc = ctx.createOscillator();
      var gain = ctx.createGain();
      gain.gain.value = 0.001;
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      console.log('[OTO] KeepAlive ses basladi (Chrome sekmeyi uyutamaz)');
    } catch (_) {}
  }

  function pacsSaglikKontrol(cb) {
    var testBtn = findButtonByText(['Bugün', 'Bugun', 'Today']);
    if (!testBtn) { cb(false); return; }
    testBtn.click();
    var kontrol = 0;
    var timer = setInterval(function () {
      kontrol++;
      var rows = document.querySelectorAll('tr');
      var found = false;
      for (var i = 0; i < rows.length; i++) {
        if ((rows[i].innerText || '').indexOf('BT') >= 0 || (rows[i].innerText || '').indexOf('MR') >= 0 || (rows[i].innerText || '').indexOf('CR') >= 0) {
          found = true; break;
        }
      }
      if (found) { clearInterval(timer); cb(true); }
      else if (kontrol >= 10) { clearInterval(timer); cb(false); }
    }, 1000);
  }

  function otoDevam() {
    log('PACS kontrol ediliyor...', 'orange');
    pacsSaglikKontrol(function (ok) {
      if (ok) {
        log('PACS calisiyor! 10sn sonra devam edecek...', 'lime');
        setTimeout(function () { OTO.baslat(); }, 10000);
      } else {
        log('PACS henuz hazir degil. 5dk sonra tekrar deneyecek...', 'orange');
        setTimeout(function () { otoDevam(); }, 300000);
      }
    });
  }

  function init() {
    OTO._renderUI();
    var s = GM.get('STATE', null);
    if (s && s.aktif) {
      var compCount = Object.keys(getCompleted()).length;
      log('Onceki oturum: ' + s.i + '/' + HASTALAR.length + ' (OK:' + compCount + ' ERR:' + s.hata.length + ')', '#888');
      log('PACS kontrol ediliyor, hazir olunca otomatik devam edecek...', 'cyan');
      setTimeout(function () { otoDevam(); }, 5000);
    } else {
      log('Hazir. BASLAT butonuna bas (veya konsol: OTO.baslat())', 'cyan');
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
