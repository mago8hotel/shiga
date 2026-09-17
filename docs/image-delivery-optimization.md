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

CSS背景なので遅延読み込みされず、初期ロードで3枚とも通信する。表示幅は1440px時273px / 820px時233px /
375px時335pxなので、元データ幅を1000pxで頭打ちにした。

`shizen.webp` は元が700×1050で既に1000px以下のため縮小していない。ファイルサイズが269,690バイトと
大きいのは元写真の粒状感によるもので、幅の縮小では減らせない。画質を落とさずに減らす方法がないため
今回は据え置いた。

`image-set()` は使っていない。同じURLのまま中身だけ小さくしたので、CSSの記述は変更なし。

### 容量

| ファイル | 変更前 bytes | 変更後 bytes | 寸法 |
|---|---:|---:|---|
| assets/images/120.webp | 186,080 | 105,204 | 1400×788 → 1000×563 |
| assets/images/taiken.webp | 126,838 | 67,978 | 1567×1045 → 1000×667 |
| assets/images/shizen.webp | 269,690 | 269,690 | 700×1050（変更なし） |
| assets/images/moji-1362.webp | （新規） | 29,842 | 1362×454 |

- 魅力カード3枚合計：582,608 → 442,872 bytes（139,736 bytes / 24.0%削減）。
- heroロゴ：DPR2の820px幅・1440px幅では 162,768 → 29,842 bytes（132,926 bytes削減）。
  375px幅では従来どおり780pxのWebPが選ばれるため変化なし。
- 元画像（moji.jpg / 120.jpg / taiken.jpg / shizen.jpg）は変更していない。ライトボックスは従来どおり元JPEGを開く。

### 画質（変更前後のWebPを同じ表示サイズにcoverで合わせて比較）

| 画像 | 1440@2x | 820@2x | 375@3x |
|---|---|---|---|
| 120.webp | PSNR 39.96dB / SSIM 0.987 | 38.21dB / 0.983 | 32.39dB / 0.957 |
| taiken.webp | PSNR 45.40dB / SSIM 0.993 | 44.68dB / 0.992 | 42.47dB / 0.986 |

375px幅の3倍密度が最も条件が厳しく、120.webpで1.5倍の拡大になる。カードは暗いグラデーションの
オーバーレイ越しの背景写真であり、ブラウザ表示では差を確認できなかった。
