Silva HAMA | Portfolio（静的HTML版 / rev.4 GitHub Pages 対応）
==================================================

Figma プロトタイプ「PortFolio」を HTML / CSS / JavaScript で再現・清書した静的サイトです。
rev.3（2026-11-18）で、GitHub Pages にそのままアップロードして公開できるフォルダ構成にしました。
rev.4（2026-11-18）で、Profile ページ（ホバー時の写真・職歴・スキル一覧）を更新しました。

■ このフォルダの中身
  docs/        公開するサイト本体（この「中身」を GitHub に置きます）
  _src/        生成元データ（文言の修正・再生成用。公開には不要）
  README.txt   このファイル（公開には不要）
  .gitignore   Git を使う場合用（公開には不要）

■ GitHub Pages で公開する手順（ブラウザだけで完結します）
  事前に：GitHub アカウントが必要です（メールアドレスの認証を済ませてください）。
  無料プラン（GitHub Free）では、GitHub Pages を使えるのは「Public（公開）」リポジトリだけです。

  1. リポジトリを作る
     github.com 右上の「＋」→「New repository」
       ・Repository name … 例：portfolio（この名前が公開 URL の一部になります）
       ・Public を選ぶ
       ・「Create repository」を押す

  2. docs フォルダの「中身」を 5 回に分けてアップロードする
     GitHub のブラウザアップロードは 1 回 100 ファイルまでのため、次の 5 回に分けてあります。
     作成直後の画面にある「uploading an existing file」のリンク
     （表示が違う場合や 2 回目以降は「Add file」→「Upload files」）を開き、
     下の単位でドラッグ＆ドロップ →「Commit changes」を押す、を 5 回繰り返します。

       1 回目  index.html / profile.html / works.html / 404.html / favicon.svg / .nojekyll
               ＋ assets フォルダ ＋ works フォルダ      （66 ファイル）
       2 回目  img-ai フォルダ                           （32 ファイル）
       3 回目  img-digital フォルダ                      （78 ファイル）
       4 回目  img-other フォルダ                        （67 ファイル）
       5 回目  img-web フォルダ                          （76 ファイル）

     ※ フォルダは必ず「ドラッグ＆ドロップ」で入れてください（フォルダ構成が保たれます。
        「choose your files」のファイル選択ではフォルダごと選べません）。
     ※ docs フォルダそのものではなく、docs の「中身」をリポジトリの一番上の階層に置きます。
        アップロード後、リポジトリの最初の画面に index.html が見えていれば正解です。
     ※ .nojekyll は Mac では隠しファイルです（Finder で Command + Shift + .（ピリオド）を押すと見えます）。
        入れ忘れても表示が変わらないことは確認済みですが、入れておくと確実です。
        後から足す場合：「Add file」→「Create new file」→ ファイル名に .nojekyll と入力 →「Commit changes」。
     ※ ボタンが「Commit changes」ではなく「Propose changes」と表示される場合もあります。
     ※ Mac では「.DS_Store」という隠しファイルが一緒にアップロードされることがあります。表示には影響しません
        （その分を足しても、各回 100 ファイル以内に収まります）。

  3. GitHub Pages を有効にする
     リポジトリの「Settings」→ 左メニューの「Pages」→「Build and deployment」
       ・Source … Deploy from a branch
       ・Branch … main、フォルダは / (root) →「Save」を押す

  4. 公開されるのを待つ（最長で 10 分ほど）
     同じ「Pages」の画面に公開 URL と「Visit site」ボタンが表示されます。
       URL：https://＜ユーザー名＞.github.io/＜リポジトリ名＞/
     （リポジトリ名を「＜ユーザー名＞.github.io」にすると https://＜ユーザー名＞.github.io/ で公開されます）

  ● Git を使う場合（こちらでも公開できます）
     このフォルダ全体をそのままリポジトリにして push し、手順 3 のフォルダを「/docs」にします。
       git init -b main
       git add .
       git commit -m "Publish portfolio"
       git remote add origin https://github.com/＜ユーザー名＞/＜リポジトリ名＞.git
       git push -u origin main
     ※ この方法では _src/ と README.txt もリポジトリ（Public）に入ります。

  ● 公開前に知っておくこと
     ・Public リポジトリに置いたファイルは、だれでも見られます。
     ・サイトにはメールアドレス（mailto リンク）と Instagram へのリンクが載っています。
     ・rev.2 で追加した 3 作品（works/digital-7・web-7・other-5）の画像は第三者の公開素材です（画像の下にクレジットを表示）。
       Public リポジトリに置いた時点でだれでも見られる状態になるため、アップロードの前に掲載可否の確認をお願いします。
     ・サイトの容量は約 30 MB です（GitHub Pages の上限は 1 GB）。

  ● 公開後に更新するには
     直したファイルを同じ場所へアップロードし直すと上書きされます（反映まで最長 10 分ほど）。
     古い表示が残るときは、ブラウザで再読み込みしてください。

  ● GitHub Pages 向けに確認したこと（2026-11-18。rev.4 のファイルで再確認済み）
     ※ 実際の GitHub にはアップロードしていません。GitHub Pages の配信ルール（大文字小文字の区別、フォルダ URL、
        拡張子なし URL、404.html）を再現した確認環境での結果です。
     ・リンクと画像の参照はすべて相対パスです。https://…github.io/＜リポジトリ名＞/ の形でも、
       独自ドメインや ＜ユーザー名＞.github.io の直下でも、そのまま動きます
       （両方の形で、Chromium・Firefox・WebKit の 3 種類のブラウザでページ移動・404・転送を確認）。
     ・ファイル名は半角の英小文字・数字・ハイフン・ピリオドのみ、大文字小文字の食い違いなし
       （GitHub Pages は大文字小文字を区別します）。
     ・1 ファイルの大きさは最大 約 1.5 MB です（ブラウザからのアップロード上限は 1 ファイル 25 MiB）。
     ・.nojekyll が無い場合も、GitHub Pages が使う Jekyll 3.10.0（github-pages 232）でビルドして、
       サイトの全 318 ファイルが 1 バイトも変わらずに出力されることを確認しています
       （この場合、GitHub の既定テーマの assets/css/style.css が 1 つ余分に出力されますが、サイトからは参照しません）。

■ アップロード前に手元で確認するには
  docs フォルダの index.html をブラウザで開いてください（すべて相対パスのため、そのまま表示されます）。

■ rev.4 の変更点（2026-11-18／Profile ページのみ）
  ・プロフィール写真：マウスを乗せたとき（スマートフォンではタップしたとき）に表示される写真を、
    ご支給の画像に差し替えました（docs/assets/img/profile-alt.webp）。
      ご支給の画像は 659×658px のため、左端の 1px を落として正方形 658×658px にし、WebP に変換しています。
      通常時の写真と、TOP ページのプロフィール写真は変えていません。
  ・職歴：最後の行「2025年 現在に至る」を、次の内容に更新
      2025年  株式会社ピラミッドフィルムクアドラ 退社
        ↓
      2025年  株式会社テー・オー・ダブリュー 入社
              体験デザイン本部デジタルアクティベーション室プロデューサー
              現在に至る
    ※ 所属・肩書きの行は、画面が狭いとき「体験デザイン本部／デジタルアクティベーション室／プロデューサー」の
       区切りで折り返します（幅 320px のスマートフォンまで、区切り以外の位置では切れないことを確認）。
  ・Skill Set の「ソフトウェア」に 6 件追加（既存の項目の後ろに、いただいた順で追加）
      Microsoft Office
        Microsoft Teams    基本的な操作、チャット、チーム機能
        Microsoft Outlook  基本的な操作
      Generative AI
        Claude             基本的な操作、簡単なプロンプトの設計、資料、HTML生成
        Seedance           基本的な操作、動画生成
        Gemini             基本的な操作、画像生成、動画生成 (Veo)
        Muse               基本的な操作、リマインド、Webブラウザベースの自動化、スペース
  ・変更したファイルは docs の中の次の 3 つだけです（ほかの 316 ファイルは rev.3 と 1 バイトも変わっていません）。
      profile.html ／ assets/css/site.css ／ assets/img/profile-alt.webp
  ・すでに rev.3 を GitHub にアップロード済みの場合
      リポジトリの最初の画面で「Add file」→「Upload files」を開き、docs の中の profile.html と assets フォルダ
      （合わせて 38 ファイル）をドラッグ＆ドロップ →「Commit changes」。同じ名前のファイルが上書きされます
      （反映まで最長 10 分ほど。古い写真が出るときはブラウザで再読み込みしてください）。

■ rev.3 の変更点
  ・肩書き：TOP ページ（2 か所）と Profile ページ（1 か所）の肩書きの最後に「プロデューサー」を追加
    （TOP ページの説明文＝検索結果や SNS 共有時に出る文章も同じ表記に更新）
      プランナー・ディレクター・クリエイティブディレクター・プロデューサー
  ・追加 3 作品の Position（役割）を記入
      works/digital-7.html  デジタルアクティベーションプロデューサー
      works/web-7.html      プロデューサー・クリエイティブディレクター・プランナー
      works/other-5.html    プロデューサー
  ・肩書きは「・」の位置で折り返すようにしました（スマートフォンで単語の途中では切れません）。
    肩書きが長くなったため、幅 375px 未満の小さな画面では、TOP の肩書き横の緑の線を肩書きの上に移しています。
  ・GitHub Pages 用に追加：.nojekyll、404.html（存在しない URL 用のページ）、
    works/index.html（…/works/ にアクセスされたとき works.html へ転送）
  ・GitHub Pages 用に変更：
      作品画像の場所  assets/img/works/＜作品＞/ → img-digital/ img-web/ img-ai/ img-other/ の下
                      （1 回 100 ファイルまでのアップロード制限に収めるため）
      CSS のファイル名  assets/css/style.css → assets/css/site.css
                      （.nojekyll が無い場合に GitHub Pages の既定テーマが同じ名前のファイルを出力するため）
  ・上記以外の見た目・文言・リンク先・画像は rev.2 から変えていません
    （rev.2 と全ページの文言・リンク・画像ファイルを機械的に突き合わせて確認）。

■ docs/ の構成（HTML 27 ファイル ＝ 25 ページ ＋ 404 ＋ 転送用 1 ／ 全 319 ファイル）
  index.html               Landing（Profile / Works / Contact）
  profile.html             Profile（経歴 / Skill Set / Hobby）
  works.html               Works 一覧（Digital / Web / AI / Other）
  works/digital-1〜7.html  Digital Contents 作品詳細（7 ページ）
  works/web-1〜7.html      Web Contents 作品詳細（7 ページ）
  works/ai-1〜3.html       AI Contents 作品詳細（3 ページ）
  works/other-1〜5.html    Other Creative 作品詳細（5 ページ）
  works/index.html         …/works/ から works.html への転送用
  404.html                 存在しない URL にアクセスされたときのページ
  .nojekyll                GitHub Pages に「ファイルをそのまま公開する」と伝える空ファイル
  favicon.svg              ファビコン
  assets/css/site.css      スタイル（レスポンシブ対応）
  assets/js/main.js        ローディング / ページ遷移 / スクロール演出 / プロフィール画像切替 / 画像ライトボックス
  assets/img/              共通の画像（ヒーロー・プロフィール・Hobby・装飾・背景）
  img-digital/ img-web/ img-ai/ img-other/
                           作品の画像（カテゴリー別 → 作品別）
  画像は WebP 287 点・SVG 2 点です。

■ 文言やリンクを修正するには
  1. _src/content.json（文言・ページ構成・リンク）を編集
  2. Python 3 で「pip install jinja2」を実行後、「python3 _src/build.py」を実行
     （docs/ の HTML 27 ファイルと .nojekyll を作り直します）
  3. docs/ 直下の HTML と works フォルダを GitHub にアップロードし直す
  ※ 肩書きの場所：TOP・Profile 共通は "about" → "roles"、作品ごとは "works" → 各作品 → "role"。
     「・」で区切って書くと、その位置で折り返します。
  ※ 職歴の場所："about" → "history" → "career"。"year" を null にすると、年を表示しない行（「現在に至る」）になります。
     "detail" を ["A", "B"] のように配列で書くと、その区切りの位置でだけ折り返します。
  ※ スキル一覧（ソフトウェア）の場所："about" → "software"。
  ※ プロフィールのホバー時の写真は、docs/assets/img/profile-alt.webp を同じファイル名で置き換えます（正方形の画像）。
     画像の大きさを変えた場合は、_src/assets.json の "profile_alt" の w / h も合わせてから build.py を実行してください。
  ※ docs/ の HTML を直接編集しても構いませんが、build.py を再実行すると上書きされます。
  ※ タグ文字・矢印・サインは _src/svg/*.svg を各ページにインラインで埋め込んでいます（色は CSS の color で指定）。
  ※ CSS（docs/assets/css/site.css）と JavaScript（docs/assets/js/main.js）は直接編集します。

■ 外部依存
  Web フォント（Anton / Inter / Noto Sans JP）のみ Google Fonts から読み込みます。
  オフライン時は OS 標準の書体で表示されます。

■ rev.2 のデザイン変更
  ・配色：ネオングリーンの全面グラデーション → 黒に近い「夜の壁」基調（#07070a）。
    グリーンは彩度を落とした #1fe86a をスプレーの線・アクセントに限定し、補色としてバイオレット（#7b5cff）を薄く使用。
    色は docs/assets/css/site.css 冒頭の :root（--bg / --ink / --green / --violet）で一括変更できます。
  ・グラフィティのトーン：Figma の手描きタグ文字・矢印・フレーム・サインはそのまま使用し、白（文字）とグリーン（線）に塗り分け。
    背景の壁テクスチャ（docs/assets/img/bg/wall.webp）は、このサイト自身のタグ文字から生成したオリジナルです（_src/texture.py）。
  ・見出し：Anton（極太コンデンス）によるアウトライン文字／大型タイポを追加。
  ・演出：初回ローディング（サイン＋カウンター）、ページ間のワイプ遷移、ヒーローの文字せり上がり、
    タグ文字が「書かれる」見出し、スクロールで伸びるネオンライン、背面で流れるアウトライン文字、マーキー、
    カードの番号・ホバーで発色が戻る画像 など。
    「視差効果を減らす」設定の端末と JavaScript 無効時は、演出なしで全コンテンツが表示されます。
  ・参考にしたサイトの画像・コード・フォントは使用していません（雰囲気・演出の方向性のみ参照）。

■ rev.2 で追加した作品（3 件）
  ・works/digital-7.html　TokyoGameShow 2026 Minecraft Dungeons 2 Booth
      本文の出典：TOW MAGAZINE（https://tow.co.jp/magazine/magazine-49905/）ほか公開記事
      画像：TOW MAGAZINE 掲載写真（Photo：後藤 薫）
      ※ Google スライドの内容は反映していません
         （公開記事をもとにした現在の内容のままでよいとのこと：2026-11-18 ご確認済み）。
      ※ クライアント表記「Mojang Studios」（公開記事からの表記）はご了承済み（2026-11-18）。
  ・works/other-5.html　コミックマーケット 108 IRIAM Booth
      本文の出典：PR TIMES（株式会社IRIAM プレスリリース）／Saiga NAK／EnterJam
      画像：PR TIMES 掲載のプレスリリース素材
  ・works/web-7.html　Daytona Park 19th Anniversary “19周年いくぞー祭！”
      本文の出典：PR TIMES（株式会社デイトナ・インターナショナル プレスリリース）／n2p ブログ／特設サイト
      画像：PR TIMES 掲載のプレスリリース素材、特設サイトの画面（Internet Archive 2026-02-19 保存分を表示して撮影）
      ※ タイトルは 17th / 18th の表記（“ ” 囲み）に合わせています。
      ※ n2p の URL は該当記事の個別 URL（/blog/campaign/20260304/）です（ご了承済み 2026-11-18）。
  3 件の本文は公開記事をもとに作成したものです。
  3 件の画像は第三者の公開素材です。公開前に、掲載可否の確認（またはご自身の素材への差し替え）をお願いします。
  画像下のクレジットは _src/content.json の "credit" で編集・削除できます。

■ Figma から清書した表記
  ・Posision → Position（19 箇所）
  ・Chainsmorkers → Chainsmokers（2 箇所）
  ・受賞表記の余分な記号・空白を整理（1 箇所）
  ・OWEND WORK → OWNED WORK（1 箇所）
  ・Adobe Premier Pro → Adobe Premiere Pro（1 箇所）
  ・スキル一覧の重複行（Adobe Illustrator）を1行に統合（1 箇所）
  ・「Uprint)」の対応しない閉じ括弧を削除（1 箇所）
  ・ELGOO Mars Pro → ELEGOO Mars Pro（1 箇所）
  ・（rev.2）web-7 のタイトル「--19周年いくぞー祭！-」→ “19周年いくぞー祭！”（17th / 18th と同じ表記）
  ・（rev.3）web-7 の役割「プロデューサー、クリエイティブディレクター、プランナー」→「・」区切り（他の作品と同じ表記）

■ 外部リンクについて（2026-11-18 確認）
  リンク先の URL は rev.2 から変えていません。サイト内の外部リンク 25 件（ほかにメールリンク 1 件）を、
  自動操作のブラウザ（ヘッドレス Chromium）で開いた結果です。自動アクセスはボット対策で止められることがあるため、
  公開前に一度、ご自身のブラウザでクリックしてご確認ください。

  ● 要確認（1 件）
    ・works/digital-1.html  https://group.isuzu-global.com/jms/2023/
        確認環境では SSL 証明書が期限切れ（有効期限 2026-10-21）で、ブラウザが警告を表示する状態でした。
        ページ自体は残っています（証明書の検証を外すと「ISUZU / UD TRUCKS JAPAN MOBILITY SHOW 2023」が返ります）。
        リンクを残すかどうか、ご判断ください。

  ● 自動操作のブラウザでは開けなかったが、別の取得方法では該当ページの内容を確認できたもの（7 件）
    ・works/digital-4.html  https://www.sony.com/ja/SonyInfo/design/stories/communicationdesign/  （403）
    ・works/digital-6.html  https://lesdudis.com/2017/07/24/the-spider-man-homecoming-experience-sony-square-nyc/  （403）
    ・works/digital-7.html  https://www.minecraft.net/ja-jp/article/dungeons-ii-battle-for-tokyo-jp  （接続エラー）
    ・works/other-4.html    https://x.com/41pxHQ  （403）
    ・works/web-5.html      https://www.daytona-park.com/cp/17thcp/  （403）
    ・works/web-6.html      https://www.daytona-park.com/cp/18thcp/  （403）
    ・works/web-7.html      https://www.daytona-park.com/cp/19thcp/  （403）

  ● 別の URL へ転送されるもの（3 件）
    ・works/digital-5.html  https://www.pokemon.co.jp/shop/pokecen/tohoku/
        → https://shop.pokemon.co.jp/ja/shop/pokemoncenter-tohoku/（ポケモンセンタートウホク）へ転送
    ・works/web-3.html      https://lidea.today/shindan/oralitemnavi_2025
        → 現行版（…/shindan/oralitemnavi_202611「オーラルアイテムナビ｜LION」）へ転送。ご担当時の内容と同じかご確認ください
    ・全ページ共通          https://www.instagram.com/silva_h2
        → ログイン画面へ転送（未ログインの自動アクセスのため。プロフィール画面は確認できていません）

  ● そのまま表示されたもの（14 件）
    ・works/ai-1.html       https://prtimes.jp/main/html/rd/p/000000140.000049143.html
    ・works/ai-2.html       https://pfq.jp/works/yorodesu/
    ・works/ai-3.html       https://media.dglab.com/2024/01/24-rem-01/
    ・works/digital-2.html  https://prtimes.jp/main/html/rd/p/000000491.000016220.html
    ・works/digital-3.html  https://kochikame-kinenkan-official.jp/
    ・works/digital-7.html  https://tow.co.jp/magazine/magazine-49905/
    ・works/other-3.html    https://www.41military.com/html/page10.html
    ・works/other-5.html    https://enterjam.com/archives/360053
    ・works/other-5.html    https://prtimes.jp/main/html/rd/p/000000049.000070082.html
    ・works/other-5.html    https://saiganak.com/ja/event/comiket-108-iriam-booth-report/
    ・works/web-1.html      https://www.oricon.co.jp/special/71349/
    ・works/web-2.html      https://www.jwu.ac.jp/unv/
    ・works/web-4.html      https://storesolutionx.co.jp/
    ・works/web-7.html      https://n2p.co.jp/blog/campaign/20260304/
