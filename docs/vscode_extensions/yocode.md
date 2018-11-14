# Yo Code - Extension Generator
([このページ](https://code.visualstudio.com/docs/extensions/yocode)を勝手に翻訳したものです。2018-11-10)

VS Code extension を作成するには、私たちが用意した [Yeoman generator](https://github.com/Microsoft/vscode-generator-code) をお使いください。

<a id="_prerequisites"></a>
## Prerequisites

[Node.js](https://nodejs.org/en/) をインストールし、`$PATH` を通しておきます。extension generator をインストールするには、Node.js に含まれている [npm](https://www.npmjs.com/) (Node.js Package Manager) を使います。

<a id="_install-the-generator"></a>
## Install the Generator

command prompt から Yeoman と VS Code Extension generator をインストールします。
```
npm install -g yo generator-code
```

<a id="_run-yo-code"></a>
## Run Yo Code

Yeoman generator は対話形式で、customization や extension を作るのに必要な情報を聞いてきます。

generator を起動するには、command prompt で以下のように入力します。
```
yo code
```
![yo code output](https://code.visualstudio.com/assets/docs/extensions/yocode/yocode.png)

<a id="_generator-options"></a>
## Generator Options

generator では、新規 extension 用の skeleton を作る事ができます。また、TextMate definition files を元に、特定の言語やテーマ、スニペットのための extension を作る事もできます。

<a id="_new-extension-typescript"></a>
### New Extension (TypeScript)

'hello world' というコマンドを実装済みの、extension skeleton が作れます。これを元に自作の extension を作っていきます。

- extension identifier を聞かれ、入力した名前でサブフォルダが作られます。
- source, test, output フォルダといった、基本的な構造が作られます。
- `package.json` と extension main file が、テンプレートから作られます。
- `launch.json` と `tasks.json` が準備され、F5 で compile と実行、デバッガの接続ができるようになります。
- Git repository が作られます (作らせない事もできます)。

skeleton ができたら、そのフォルダを VS Code で開きます。先へ進むためのガイドは、フォルダ内の `vsc-extension-quickstart.md` に書かれています。extension API 用の IntelliSense が使えるように extension が準備されています。

<a id="_new-extension-javascript"></a>
### New Extension (JavaScript)

`New Extension (TypeScript)` と同じですが、TypeScript ではなく JavaScript が使われます。extension API 用の IntelliSense が使えるように extension が準備されています。

<a id="_new-color-theme"></a>
### New Color Theme

新規 color theme のための extension が作れます。既存の TextMate color theme を元にして作る事もできますし、ゼロから作る事もできます。

- __Developer: Generate Color Theme From Current Settings__ コマンドを使って、自分で colors を設定して theme を作るなら、新規 extension を作るところから始めます (推奨)。
- すでに `.tmTheme` ファイル (TextMate color theme) があるなら、それを元に作る事もできます。

generator は以下の事をします。

- color theme 名と、color base theme (light または dark) を聞いてきます。
- extension identifier を聞いてきます。入力した名前でサブフォルダが作られます。

できた extension のフォルダを VS Code で開いて、theme を試すために extension を実行しましょう。`vsc-extension-quickstart.md` には、先へ進むためのガイドが書いてあります。

<a id="_new-language-support"></a>
### New Language Support

言語に colorizer を付けるための extension が作れます。

- 既存の TextMate language file (.tmLanguage, .plist or .json) の場所 (URL またはファイルパス) を聞いてきます。選択したファイルが、作成する extension に読み込まれます。文法をゼロから作る場合は、何も入力せずに次へ進みます。
- extension identifier を聞いてきます。入力した名前でサブフォルダが作られます。

できた extension のフォルダを VS Code で開いて、colorization を試すために extension を実行しましょう。`vsc-extension-quickstart.md` には、先へ進むためのガイドが書いてあります。生成された language configuration file を見てみましょう。その言語で使われるコメントや括弧のスタイルが、設定されているのが分かります。

<a id="_new-code-snippets"></a>
### New Code Snippets

新しい code snippets のための extension が作れます。

- TextMate snippets (.tmSnippet) または Sublime snippets (.sublime-snippet) が置かれているフォルダの場所を聞いてきます。それらのファイルを VS Code snippet file に変換します。
- snippets をアクティブにしたい言語を聞いてきます。
- extension identifier を聞いてきます。入力した名前でサブフォルダが作られます。

できた extension のフォルダを VS Code で開いて、snippets を試すために extension を実行しましょう。`vsc-extension-quickstart.md` には、先へ進むためのガイドが書いてあります。