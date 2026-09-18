# 画像配信最適化（PRレビュー用）

## 目的・方法

写真・文章・レイアウトを維持して、小さな画像の転送量を削減する。

- 元画像は変更・削除しない。18サムネイルは216px角（72px表示の3倍）、スタンプ2枚は240px角（80px表示の3倍）。既存の中央 `object-fit: cover` と同じ構図。
- `data-full` に元画像を指定し、ライトボックスは元の高解像度JPEGを開く。詳細パネルの写真は従来どおり。
- top/120/taiken/shizen/kominka は元と同寸法のWebP quality=88。ヒーロー背景とpreloadは同じWebPを参照。
- ロゴは342px（ナビ）・780px（ヒーロー）に縮小後、lossless WebPで保存。縮小自体は可逆ではない。大画面・高DPRでは `srcset` に残した2172pxの元JPEGを選択できる。CSSの反転・ブレンド・サイズは変更しない。
- heroロゴはlazyにしない。その他のlazy設定、動画、SEO、予約リンク、アニメーションは変更しない。
- Pillow 11.3.0で生成。再生成は `python3 scripts/optimize_images.py`。ビルド時の処理やブラウザ向け依存追加なし。

## 容量（実ファイルのバイト数）

| 元画像 | 配信用画像 | 変更前 bytes | 変更後 bytes |
|---|---|---:|---:|
| top.jpg | assets/images/top.webp | 321,575 | 268,190 |
| 120.jpg | assets/images/120.webp | 215,888 | 186,080 |
| taiken.jpg | assets/images/taiken.webp | 226,660 | 126,838 |
| shizen.jpg | assets/images/shizen.webp | 272,807 | 269,690 |
| kominka.jpg | assets/images/kominka.webp | 242,567 | 229,148 |
| moji.jpg | assets/images/moji-342.webp | 162,768 | 17,362 |
| moji.jpg | assets/images/moji-780.webp | 162,768 | 69,060 |
| dokutu.jpg | assets/images/dokutu-thumb.webp | 226,060 | 9,472 |
| taiken.jpg | assets/images/taiken-thumb.webp | 226,660 | 11,360 |
| hoshi.jpg | assets/images/hoshi-thumb.webp | 285,998 | 6,518 |
| kaya2.jpg | assets/images/kaya2-thumb.webp | 160,773 | 6,582 |
| ana.jpg | assets/images/ana-thumb.webp | 370,455 | 19,530 |
| raku.jpg | assets/images/raku-thumb.webp | 161,150 | 20,590 |
| chie.jpg | assets/images/chie-thumb.webp | 286,197 | 11,600 |
| kawa.jpg | assets/images/kawa-thumb.webp | 419,495 | 21,174 |
| mushi.jpg | assets/images/mushi-thumb.webp | 381,915 | 17,822 |
| gyara.jpg | assets/images/gyara-thumb.webp | 278,121 | 12,238 |
| kotatu.jpg | assets/images/kotatu-thumb.webp | 145,667 | 15,408 |
| hotaru.jpg | assets/images/hotaru-thumb.webp | 357,088 | 14,454 |
| BBQ1.jpg | assets/images/BBQ1-thumb.webp | 172,342 | 16,736 |
| akuse1.jpg | assets/images/akuse1-thumb.webp | 145,879 | 14,800 |
| akuse2.jpg | assets/images/akuse2-thumb.webp | 174,099 | 17,236 |
| p.jpg | assets/images/p-thumb.webp | 706,528 | 11,998 |
| stamp1.jpg | assets/images/stamp1-thumb.webp | 209,926 | 16,612 |
| stamp2.jpg | assets/images/stamp2-thumb.webp | 214,211 | 18,270 |

### 合計の読み方

- 18サムネイル用途の合計：4,922,564 → 262,400 bytes（94.7%削減）。
- 変更対象のユニーク画像集合：6,138,169 → 1,428,768 bytes（4,709,401 bytes / 76.7%削減）。スマホで780pxロゴを選択し、詳細・ライトボックスを開かず、対象写真まで閲覧する条件。ページ全体の実測ネットワーク転送量ではない。
- トップ背景＋ロゴ：484,343 → 354,612 bytes（26.8%削減、780pxロゴ選択時）。変更前は同じmoji.jpgをナビとheroで共有しているため1回だけ数えた。
- 高DPRの大画面で元ロゴを選択した場合、ロゴ用途は元JPEG＋ナビWebPとなり17,362 bytes増える。ただしトップ背景と合わせると484,343 → 448,320 bytesに減る。画質優先のトレードオフ。
- 元画像も残すのでリポジトリ容量は約1.43MB増加する。拡大表示時には元画像が追加ロードされる。
- CSS背景は従来同様lazy対象外。下方の写真はネイティブlazyで、ブラウザにより先読み範囲が異なる。

## ローカル検証

- 1440×1000 / 820×1000 / 375×812でブラウザ目視：トップ写真、白いロゴ、魅力カード、体験のサムネイルを確認。既存の構図・文字配置を維持。
- 1440 / 820 / 375各幅で変更前後のDOM寸法を比較：ロゴ、魅力カード、体験サムネイルの寸法一致。
- 魅力カードの高さ（CSS px四捨五入）：1440幅=238 / 820幅=262 / 375幅=251。各行の高さは変更前と一致。
- 初期アニメーション終了後のページ幅は1440 / 820 / 375。初期の一時的な横幅超過は既存仕様のまま（今回の範囲外）。
- 820pxで洞窟サムネイルから1045×1567のdokutu.jpgをライトボックス表示。
- 375pxで「詳細を見る」から里山散策詳細を開き、1162×900のsansaku.jpgが従来どおり拡大表示されることを確認。
- 新旧画像・srcset・data-full・背景を含む60参照：ファイル存在、画像デコード、ローカルHTTP200確認。
- HTMLタグ構造、表示文章、画像配信以外の属性が変更前と一致。CSS/JS差分は背景URL・ライトボックス参照先のみ。
- title/description/JSON-LD、Beds24（propid=344052）、口コミ・動画は変更なし。元画像変更なし。
- iPhone実機と高DPR実機の目視は未実施。ブラウザ幅による確認。

## PageSpeed

| 指標 | 変更前（参考・本番単発測定） | 変更後 |
|---|---:|---|
| Performance | 91 | 未測定 |
| LCP | 3.5秒 | 未測定 |
| FCP | 1.0秒 | 未測定 |
| CLS | 0 | 未測定 |
| TBT | 0ms | 未測定 |
| Speed Index | 2.7秒 | 未測定 |

このPRはmainへ未マージで、公開プレビュー環境は用意していないため、PageSpeed Insightsからローカル変更版は測定できない。本番を測定しても変更後の比較にはならない。承認後の公開時に同条件で複数回測定し、小さな差だけで効果を断定しない。

## レビュー時の注意

- 新しい派生画像を変更した場合はpreload・srcset・data-fullとの整合性を保つ。
- WebP対応の現行ブラウザが対象。非対応の古いブラウザ向けフォールバックは今回追加していない。
- デザイン・初期アニメーション・safe-areaの追加修正は含めない。
- GitHub Pagesの公開ブランチはmainのまま。作業ブランチのpush/PR作成のみで停止する。

---

## 第3フェーズ（heroロゴと魅力カード背景）

前回のレビューでMediumとして残った2件のみ。文章・レイアウト・予約導線・構造化データは変更していない。

### heroロゴ

`srcset` の候補が 780px と 2172px（元JPEG）しかなく、DPR2の1440px幅では 680 CSS px 表示に対して
1360px相当が必要なため、2172pxの元JPEGが選ばれていた。`assets/images/moji-1362.webp`（1362×454、
元と同じ3:1）を候補に追加した。1360pxちょうどではなく1362pxなのは、1359pxだと必要幅1360pxに1px足りず
元JPEGが選ばれてしまうため。

このサイズだけ lossless ではなく `quality=90` を使っている。1362pxを lossless で保存すると171,542バイトとなり
元JPEG（162,768バイト）より大きく、目的を果たせないため。表示サイズ（680px）まで縮小した状態で
lossless版と比較した最大チャンネル差は6/255、平均0.51/255。

`loading="lazy"` は付けていない。preloadは従来どおり `assets/images/top.webp` のみで、ロゴのpreloadは
元々存在しないため整合性の変更もない。`aspect-ratio: 3 / 1` と元画像の比率は一致している。

### 魅力カード背景

**結論：3枚とも main と同じファイルのまま（変更なし）。**

魅力カードは `background-size: cover` で `aspect-ratio: 4/3` の枠に表示される。横長の写真は枠の**高さ**に
合わせて拡大され、左右が切られるため、**必要な解像度は「枠の幅」ではなく「枠の高さ × DPR」で決まる**。

倍率 = max(枠幅 ÷ 画像幅, 枠高 ÷ 画像高) × DPR（1.00を超えると引き伸ばし）

実測した枠の大きさ（CSS px）：375px 335×251.3 / 393px 353×264.8 / 430px 390×292.5 /
744px 704×528 / 768px 728×546 / 820px 233×262 / 1440px 273×238。769px未満は1列表示で、
枠は「画面幅−40px」×その3/4になるため、タブレット縦向きで最も大きくなる。

| 画像（main・本PR共通） | 375@3x | 393@3x | 430@3x | 744@2x | 768@2x | 820@2x | 1440@2x |
|---|---:|---:|---:|---:|---:|---:|---:|
| 120.webp 1400×788 | 0.96 | 1.01 | 1.11 | 1.34 | 1.39 | 0.66 | 0.60 |
| taiken.webp 1567×1045 | 0.72 | 0.76 | 0.84 | 1.01 | 1.04 | 0.50 | 0.46 |
| shizen.webp 700×1050 | 1.44 | 1.51 | 1.67 | 2.01 | 2.08 | 0.67 | 0.78 |

このPRの途中で縮小を2回試し、どちらもレビューで取り下げた。

- 1回目：120 / taiken の幅を1000pxに縮小。幅で計算した誤りで、iPhone（DPR3）で120.webpが最大1.56倍に拡大された。
- 2回目：taiken を高さ880px（1320×880）に縮小。iPhoneでは等倍以下だった。しかしタブレット縦向き（744〜768px・DPR2）で
  倍率が main の1.01〜1.04から1.20〜1.24に上がり、再レビューの実測ではPSNRも42.7dBから37.3dBに下がった。削減できるのは約30KB
  （カード3枚合計の5.2%）だけで、写真の解像度を犠牲にしないという前提に合わない。

`image-set()` は使っていない。CSSの記述も変更していない。

### 既知の制約

- shizen.webp は元画像が700×1050しかなく、main の時点でタブレット縦向きに2.01〜3.12倍（744px・DPR2〜768px・DPR3）
  拡大されている。より高解像度の写真が用意できるまで改善できない。

### 容量

| ファイル | 変更前 bytes（main） | 変更後 bytes | 寸法 |
|---|---:|---:|---|
| assets/images/moji-1362.webp | （新規） | 29,842 | 1362×454 |
| assets/images/120.webp | 186,080 | 186,080 | 1400×788（変更なし） |
| assets/images/taiken.webp | 126,838 | 126,838 | 1567×1045（変更なし） |
| assets/images/shizen.webp | 269,690 | 269,690 | 700×1050（変更なし） |

- 本PRで転送量が減るのは heroロゴのみ。DPR2の820px幅・1440px幅、DPR3の820px幅で
  162,768 → 29,842 bytes（132,926 bytes削減）。
- 375〜430px幅（iPhone）、およびDPR1、1440px幅のDPR3では、選ばれるロゴが main と同じため変化しない。
- 元画像（moji.jpg / 120.jpg / taiken.jpg / shizen.jpg）は変更していない。ライトボックスは従来どおり元JPEGを開く。
