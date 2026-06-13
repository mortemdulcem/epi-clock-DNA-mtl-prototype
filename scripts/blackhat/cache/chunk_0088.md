## Özet

Birçok tasarım kararında olduğu gibi, bir işi yapmanın birden fazla yolu vardır. İster Go'nun yerleşik eklenti (plug-in) sistemini ister Lua gibi alternatif bir dili kullanın, ödünleşimleri (trade-off) dikkate almalısınız. Ancak yaklaşımınız ne olursa olsun, özellikle yerleşik eklenti sisteminin eklenmesiyle, Go'yu kolayca genişleterek zengin güvenlik çatıları (framework) oluşturabilirsiniz.

Bir sonraki bölümde, kriptografi gibi zengin bir konunun üstesinden geleceksiniz. Çeşitli uygulamaları ve kullanım senaryolarını gösterecek ve ardından bir RC2 simetrik anahtar kaba kuvvet (brute-force) aracını inşa edeceğiz.

## 11  
KRIPTOGRAFIYI UYGULAMAK VE SALDIRMAK

Kriptografiyi keşfetmeden bir güvenlik tartışması tamamlanmış sayılmaz. Kuruluşlar kriptografik uygulamalar kullandığında, bilgi ve sistemlerinin bütünlüğünü, gizliliğini ve kimliğin doğrulanmasını (doğruluk, authenticity) korumaya yardımcı olabilirler. Bir araç geliştiricisi olarak, muhtemelen SSL/TLS haberleşmesi, karşılıklı kimlik doğrulama, simetrik anahtar kriptografisi veya parola özetleme (password hashing) gibi konular için kriptografik özellikler uygulamanız gerekecektir. Ancak geliştiriciler kriptografik fonksiyonları sıklıkla güvensiz biçimde uygular; bu da saldırı odaklı kişilerin sosyal güvenlik (social security) veya kredi kartı numaraları gibi hassas, değerli verileri ele geçirmek için bu zayıflıklardan yararlanabileceği anlamına gelir.

Bu bölümde Go ile kriptografinin çeşitli uygulamalarını gösteriyor ve yararlanabileceğiniz yaygın zayıflıkları tartışıyoruz. Farklı kriptografik fonksiyonlar ve kod blokları için giriş niteliğinde bilgiler sağlasak da, kriptografik algoritmaların inceliklerini veya matematiksel temellerini keşfetmeye çalışmıyoruz. Açıkçası bu, kriptografi konusundaki ilgimizin (ve bilgimizin) çok ötesinde. Daha önce de belirttiğimiz gibi, bu bölümdeki hiçbir şeyi, sahibi tarafından açıkça izin verilmemiş kaynaklara veya varlıklara karşı denemeye kalkışmayın. Bu tartışmaları, yasadışı faaliyetlere yardımcı olmak için değil, öğrenme amaçlı olarak dahil ediyoruz.
