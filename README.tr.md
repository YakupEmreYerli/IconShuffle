<p align="center"><a href="README.md">English</a> · <b>Türkçe</b> · <a href="README.de.md">Deutsch</a> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.ja.md">日本語</a> · <a href="README.pt-BR.md">Português (Brasil)</a> · <a href="README.zh-Hans.md">简体中文</a></p>

<p align="center">
<img src="docs/assets/logo.png" width="140" height="140" alt="IconShuffle logosu: yuvasından kalkan mor cam bir simge">
</p>

<h1 align="center">IconShuffle</h1>

<p align="center">
<b>iPhone ana ekranınızı bilgisayardan düzenleyin.</b><br>
Telefonunuzun canlı aynasında gerçek simgelerinizi sürükleyin ya da ne istediğinizi yapay zekâ asistanınıza söyleyin.<br>
Windows, macOS ve Linux · USB ya da Wi-Fi · Mac, jailbreak ya da hesap gerekmez.
</p>

<p align="center">
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/%C4%B0ndir-Windows-8b6cff?logo=windows&logoColor=white" alt="Windows için indir"></a>
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/%C4%B0ndir-macOS-8b6cff?logo=apple&logoColor=white" alt="macOS için indir"></a>
<a href="https://github.com/YakupEmreYerli/IconShuffle/releases/latest"><img src="https://img.shields.io/badge/%C4%B0ndir-Linux-8b6cff?logo=linux&logoColor=white" alt="Linux için indir"></a>
</p>

<p align="center">
<a href="https://github.com/YakupEmreYerli/IconShuffle/actions/workflows/ci.yml"><img src="https://github.com/YakupEmreYerli/IconShuffle/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/lisans-MIT-blue" alt="MIT lisansı"></a>
<a href="https://iconshuffle.app"><img src="https://img.shields.io/badge/site-iconshuffle.app-ff9a4d" alt="iconshuffle.app"></a>
</p>

<p align="center"><a href="https://iconshuffle.app">Web sitesi</a> · <a href="docs/agent-guide.md">Asistan rehberi</a></p>

<picture>
<source media="(prefers-color-scheme: dark)" srcset="docs/assets/demo-dark.gif">
<img src="docs/assets/demo-light.gif" alt="IconShuffle demosu: düzenleyici bir deneme iPhone'unu gösteriyor; A-Z sırala simgeleri dizer, değişiklik listesi dolar ve Uygula'ya basılana kadar telefona hiçbir şey yazılmaz">
</picture>

Altı inçlik ekranda altmış simgeyi tek tek sürüklemek, üstelik simgeler titreyip birbirini
sonraki sayfaya iterken, kimsenin sevdiği bir iş değil. IconShuffle ana ekranınızı gerçek
simgeleri, klasörleri ve widget'larıyla bilgisayarın büyük ekranına taşır; düzeni orada
kurarsınız. Uygula'ya basmadan telefona hiçbir şey gitmez. Her yazmadan önce yedek alınır,
yazmadan sonra telefon yeniden okunur ve planla uyuşmazsa eski düzen kendiliğinden geri
yüklenir.

## Kurulum

**Windows** (PowerShell):

```powershell
irm https://iconshuffle.app/install.ps1 | iex
```

**macOS ve Linux:**

```bash
curl -fsSL https://iconshuffle.app/install.sh | sh
```

Betikler bu depodaki son sürümü indirip kurar. İsterseniz önce okuyun:
[`install.ps1`](install.ps1), [`install.sh`](install.sh). Kurulum dosyasını kendiniz de
[sürümler sayfasından](https://github.com/YakupEmreYerli/IconShuffle/releases/latest)
indirebilirsiniz: `IconShuffle-*-windows-x64-setup.exe`, `IconShuffle-*-macos-arm64.dmg`
ya da `IconShuffle-*-linux-x86_64.AppImage`.

Terminali mi seviyorsunuz? Komut satırı aracı bir Python paketi:

```bash
uv tool install git+https://github.com/YakupEmreYerli/IconShuffle
# ya da
pipx install git+https://github.com/YakupEmreYerli/IconShuffle
```

Kurulum dosyaları henüz imzalı değil, bu yüzden ilk açılışta bir tıklama fazladan gerekir.
macOS'ta: Sistem Ayarları → Gizlilik ve Güvenlik → **Yine de Aç**. Windows'ta SmartScreen
bir kez sorabilir: **Ek bilgi → Yine de çalıştır**.

## Üç kullanım yolu

**Uygulama.** IconShuffle'ı açın ve iPhone'u takın. Ana ekranınızı kendi simgeleri ve duvar
kâğıdıyla görürsünüz. Uygulamaları sayfalar arasında ve Dock'a sürükleyin, klasör yapmak
için bir uygulamayı ötekinin üstüne bırakın, Uygulama Arşivi'nden uygulama çekin ya da
**A-Z sırala**'ya basın. Sağ taraf her değişikliği sade bir dille listeler. **Uygula**
hepsini yazar.

**Yapay zekâ asistanınız.** Claude Code, Codex, Cursor ya da başka bir kodlama asistanı
bütün işi sizin yerinize yapabilir. Şunu yapıştırın, sonuna kendi isteğinizi yazın:

```text
https://github.com/YakupEmreYerli/IconShuffle/blob/main/docs/agent-guide.md dosyasını oku
ve iconshuffle ile iPhone ana ekranımı düzenlememe yardım et. Gerekiyorsa kur, telefona
bir şey yazmadan önce her değişikliği bana göster ve onayımı bekle. İstediğim: iş
uygulamalarımı tek bir klasöre koy, oyunları 2. sayfaya taşı.
```

[Asistan rehberi](docs/agent-guide.md) asistana aracı nasıl kurup kullanacağını anlatır;
telefona bir şey yazmadan önce değişiklikleri size göstermesi ve onayınızı beklemesi
gerektiğini de söyler. Telefonu takmak ve Güven'e dokunmak yine size kalır. Claude Code
için aynı akışı izleyen bir skill de var: [`skills/iconshuffle`](skills/iconshuffle)
klasörünü `~/.claude` içindeki `skills` klasörüne (ya da projenin `.claude` klasöründeki
`skills` klasörüne) kopyalayın.

Claude Desktop, Claude Code, Codex, Cursor, VS Code ve diğer MCP istemcileri IconShuffle'ı
bir **MCP sunucusu** olarak da kullanabilir; sunucu masaüstü uygulamasında (Python
gerekmez) ve komut satırı aracında hazır: [kurulumu](docs/mcp.md) (İngilizce) izleyin
ya da telefonsuz deneme moduyla deneyin.

**Terminal.** Düzeniniz düz bir TOML dosyası. Okuyun, istediğiniz editörde düzenleyin, yazın:

```bash
iconshuffle pull        # telefonu layout.toml dosyasına okur (yalnız okur)
iconshuffle check       # neyin değişeceğini gösterir (bağlantısız)
iconshuffle push        # sorar, yedekler, yazar, doğrular, gerekirse geri alır
```

## Güvenlik baştan düşünüldü

Ana ekran protokolünün belgesi yok ve hata affetmiyor. Bu yüzden IconShuffle göremediği bir
yazmaya asla güvenmez:

- **Önce yedek.** Her yazma, telefona dokunmadan önce mevcut düzeni kaydeder.
- **Her seferinde geri okuma.** Yazmadan sonra telefon yeniden okunur ve simge simge planla
  karşılaştırılır.
- **Kendini geri alır.** Telefon planla uyuşmazsa yedek kendiliğinden geri yüklenir.
  `iconshuffle restore latest` herhangi bir yazmayı sonradan da geri alır.
- **Yazmadan önce sorar.** Uygulamada, terminalde ya da asistanla, değişikliklerin tam
  listesini görürsünüz ve onayınız olmadan hiçbir şey yazılmaz.
- **Bilgisayarınızda kalır.** Düzenleyici yalnız 127.0.0.1 üzerinde çalışır; düzenler,
  simgeler ve yedekler bilgisayarınızdan çıkmaz. Hesap ve kullanım verisi toplama yok.

Ayrıntılar [güvenlik modeli](docs/reference.tr.md#güvenlik-modeli) bölümünde.

## Platformlar

| | Gerekenler | Durum |
| --- | --- | --- |
| **Windows 10 ve 11** (64 bit) | Microsoft Store'dan [Apple Devices](https://apps.microsoft.com/detail/9np83lwlpz9k) (ya da iTunes): USB sürücüsünü o getirir | Beta |
| **macOS** (Apple silicon) | Ek bir şey gerekmez | Beta |
| **Linux** | Kurulu ve çalışan `usbmuxd` (`sudo apt install usbmuxd`, `sudo dnf install usbmuxd`, `sudo pacman -S usbmuxd`) | Kararlı |

Motor her sistemde aynı ve testleri üç sistemde de çalışıyor. Windows ve macOS'u beta diye
işaretledik, çünkü henüz çok sayıda gerçek iPhone'la buluşmadılar. Bir kişi macOS
uygulamasını USB ile iPhone 15 Pro'da kullanıp neyin çalıştığını yazdı
([issue #6](https://github.com/YakupEmreYerli/IconShuffle/issues/6)); sizin denemeniz de
aynı ölçüde işe yarar. Her sistemde neyin otomatik denendiği
[docs/platforms.md](docs/platforms.md) sayfasında.

Her sistemde gereken tek şey bilgisayara güvenen bir iPhone: telefonu bir kez kabloyla
bağlayın, kilidini açın, **Bu Bilgisayara Güven**'e dokunun ve parolanızı girin. Wi-Fi,
USB üzerinden bir kerelik kurulumdan sonra iOS 17 ve üstünde çalışır. Root ya da
Geliştirici Modu gerekmez.

## Belgeler

- [Başvuru belgesi](docs/reference.tr.md): bütün komutlar ve seçenekler, düzen dosyası,
  düzenleyici, [güvenlik modeli](docs/reference.tr.md#güvenlik-modeli), Wi-Fi, dosyalar,
  Python API'si, sınırlar ve sorun giderme.
- [Asistan rehberi](docs/agent-guide.md): bir yapay zekâ asistanının IconShuffle'ı güvenle
  kullanması için gerekenler.
- [Platformlar](docs/platforms.md): her sistemde neyin denendiği ve beta deneyicisi olarak
  nasıl yardım edebileceğiniz.

## Katkı ve güvenlik

Kurulum, testler ve tasarımın arkasındaki tuzaklar için [CONTRIBUTING.md](CONTRIBUTING.md)
dosyasına bakın. Güvenlik sorunlarını [SECURITY.md](SECURITY.md) dosyasında anlatıldığı gibi
gizli olarak bildirin.

## Teşekkür

`ignored` listesi taşıyan sözlük yükü, [chungty/unjiggle](https://github.com/chungty/unjiggle)
projesinin 4 numaralı çekme isteğinin `setIconState` hakkında bulduklarına dayanıyor.
[facebook/idb](https://github.com/facebook/idb) içindeki ana ekran biçimi notları da yol gösterdi.
İki projeden de kod kopyalanmadı.

Cihazla iletişim [pymobiledevice3](https://github.com/doronz88/pymobiledevice3) (Wi-Fi için
RemotePairing desteği ve kullanıcı alanındaki tüneli dahil), USB erişimi libimobiledevice
projesinin [usbmuxd](https://github.com/libimobiledevice/usbmuxd) aracı üzerinden yürüyor.
Tarayıcı düzenleyicisi [Preact](https://preactjs.com) ve [htm](https://github.com/developit/htm)
ile yazıldı, [Starlette](https://www.starlette.io) ve [uvicorn](https://www.uvicorn.org) ile
sunuluyor.

## Lisans

[MIT](LICENSE). IconShuffle, GPL-3.0-or-later lisanslı pymobiledevice3'e bağımlıdır; ikisini
tek bir program olarak birlikte dağıtırsanız bu birleşim GPL kapsamına girer. Tarayıcı
düzenleyicisi Preact (MIT) ve htm (Apache-2.0) kütüphanelerinin ve IBM Plex Sans yazı tipinin
(SIL Open Font License 1.1) değiştirilmemiş kopyalarını içerir; lisansları yanlarında,
[`src/ios_homescreen/ui/static/vendor`](src/ios_homescreen/ui/static/vendor) ve
[`src/ios_homescreen/ui/static/fonts`](src/ios_homescreen/ui/static/fonts) klasörlerinde.
