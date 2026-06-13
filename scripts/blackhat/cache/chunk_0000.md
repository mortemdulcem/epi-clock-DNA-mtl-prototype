hangisi üzerinde çalışabileceğimiz bir temel. Sonuçta, bu kitap *Go ile Zarif Programlama Öğrenmek* değil — bu *Black Hat Go*.

## Giriş

Yaklaşık altı yıl boyunca, üçümüz birlikte Kuzey Amerika’daki en büyük, yalnızca sızma testine odaklanmış danışmanlık pratiklerinden birini yönettik. Baş danışmanlar olarak, müşterilerimiz adına ağ sızma testleri de dahil olmak üzere teknik proje çalışmalarını yürüttük; aynı zamanda daha iyi araçlar, süreçler ve metodolojiler geliştirilmesine öncülük ettik. Ve bir noktada, Go’yu birincil geliştirme dillerimizden biri olarak benimsedik.
    
Go, diğer programlama dillerinin en iyi özelliklerini sunar; performans, güvenlik ve kullanıcı dostuluğu arasında bir denge kurar. Kısa süre içinde, araç geliştirirken varsayılan olarak tercih ettiğimiz dil haline geldi. Zamanla, kendimizi dilin savunucuları olarak bile bulduk; güvenlik sektöründeki meslektaşlarımızı Go’yu denemeye teşvik ettik. Go’nun sunduğu faydaların, en azından değerlendirmeye değer olduğuna inanıyorduk.
    
Bu kitapta, sizi güvenlik uzmanları ve hacker’ların bakış açısından Go programlama diliyle bir yolculuğa çıkaracağız. Diğer hacking kitaplarından farklı olarak, yalnızca üçüncü taraf veya ticari araçları nasıl otomatikleştireceğinizi göstermeyeceğiz (buna biraz değinecek olsak da). Bunun yerine, daha derine ineceğiz.

---

Chris Patten

Hayat arkadaşım ve en iyi dostum Katie’ye içten bir teşekkür etmek istiyorum; sürekli desteğin, cesaretlendirmen ve bana olan inancın için. Senin ve ailemiz için yaptığın her şeyden dolayı minnettarlık duymadığım tek bir gün bile yok. Bu kadar sıkı çalışmam için bana sebep oldukları için Brooks ve Subs’a teşekkür etmek isterim. Sizin babanız olmak dünyadaki en iyi iş. Ve bir insanın isteyebileceği en iyi “ofis tazıları”na — Leo (huzur içinde yat), Arlo, Murphy ve hatta Howie’ye (evet, Howie’ye de) — evi sistematik olarak yerle bir ettiniz ve ara sıra hayat seçimlerimi sorgulamama neden oldunuz ama varlığınız ve arkadaşlığınız benim için dünyalar kadar değerli. Her birinize kemirmeniz için bu kitabın imzalı bir kopyasını vereceğim.

Dan Kottmann

Hayatımın aşkı Jackie’ye sevgisi ve cesaretlendirmesi için teşekkür ederim; desteğin ve ailemiz için yaptıkların olmasa yaptığım hiçbir şey mümkün olmazdı. Atredis Partners’taki arkadaşlarıma ve meslektaşlarıma ve geçmişte bir shell paylaştığım herkese teşekkür ederim. Bulunduğum noktadaysam, bu sizin sayenizde. Bana en başından beri inanan mentorlarıma ve arkadaşlarıma teşekkür ederim. İsimlerini tek tek sayamayacağım kadar çoksunuz; hayatımdaki inanılmaz insanlar için minnettarım. Beni bilgisayar kurslarına yazdırdığın için teşekkürler, anne (böyle şeyler vardı). Geriye dönüp baktığımda, bunlar tam bir zaman kaybıydı ve çoğu zamanı Myst oynayarak geçirdim, fakat bir merak uyandırdı (90’ları özlüyorum). En önemlisi, Kurtarıcım İsa Mesih’e teşekkür ederim.

Tom Steele

Buraya gelmek uzun bir yoldu — neredeyse üç yıl. Bu noktaya gelene kadar çok şey oldu ve işte sonunda buradayız. Arkadaşlarımızdan, meslektaşlarımızdan, ailemizden ve erken erişim okurlarından aldığımız erken geri bildirimleri içtenlikle takdir ediyoruz. Sabır gösteren siz sevgili okur, sana çok ama çok teşekkür ederiz; gerçekten minnettarız ve umarız bu kitabı yazarken aldığımız keyif kadar, siz de okurken keyif alırsınız. Her şey gönlünüzce olsun! Şimdi Go ile harika kodlar üretin!

## Teşekkür

Bu kitap, Robert Griesemer, Rob Pike ve Ken Thompson bu harika geliştirme dilini yaratmamış olsaydı mümkün olmazdı. Bu kişiler ve tüm çekirdek Go geliştirme ekibi, her sürümde sürekli olarak kullanışlı güncellemeler sunuyor. Dil öğrenip kullanması bu kadar kolay ve eğlenceli olmasaydı bu kitabı asla yazmazdık.
    
Yazarlar ayrıca No Starch Press ekibine teşekkür etmek ister: Laurel, Frances, Bill, Annie, Barbara ve birlikte çalıştığımız diğer herkes. Hepiniz, ilk kitabımızı yazmanın bakir topraklarında bize rehberlik ettiniz. Hayat devam ediyor — yeni aileler, yeni işler — ve tüm bunlar olurken sabırlı davrandınız ama yine de bu kitabı tamamlamamız için bizi motive ettiniz. No Starch Press ekibinin tamamıyla bu projede çalışmak büyük bir keyifti.
