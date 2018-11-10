# Extending Visual Studio Code
ここでは、VS Code の拡張性と、はじめての Extension を短時間で作る方法について、ご説明します。  
拡張性の設計に対する私達のアプローチについては、[こちら](https://code.visualstudio.com/docs/extensionAPI/patterns-and-principles)をご覧ください。

既存の Extension を使いたい場合は、[Extension Marketplace](https://code.visualstudio.com/docs/editor/extension-gallery) をご覧ください。VS Code [Marketplace](https://marketplace.visualstudio.com/VSCode) から Extension を探してインストールする方法をご説明しています。

すべての VS Code Extension は、contribution (registration)、activation (loading)、そして VS Code extensibility API へのアクセスといった、共通のモデルを持っています。
また、language servers と debuggers を使えるという点が重要です。これらそれぞれにアクセスするための protocol が用意されています。詳しくは以下の各セクションをご覧ください。

1. [Extensions](#_extensions) - 基本的な構成要素
1. [Language Servers](#_language-servers) - [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) を通じて、編集機能を高度に拡張します。
1. [Debuggers](#_debug-adapter) - Debug Adapter を通じて、外部デバッガを接続します。

![VS Code extensibility architecture](https://code.visualstudio.com/assets/docs/extensions/overview/extensibility-architecture.png)

<a id="_extensions"></a>
## Extensions

すべての Extension は、activate した時、Extension host process 上で実行されます。これは Extension のための分離された process で、VS Code の Main process の応答性を邪魔しません。

Extension は以下の機能を利用可能です。
- __Activation__ - 特定のファイルタイプを開いた時、特定のファイルが存在する時、または Command Palette やキーボードからコマンドが実行された時に、Extension を load する事ができます。
- __Editor__ - エディタ上のテキストやその選択状態を取得し、操作する事ができます。
- __Workspace__ - 編集中 (表示中) の各エディタやステータスバー、メッセージ等にアクセスできます。
- __Eventing__ - open, close, change など、エディタの life-cycle events を利用できます。
- __Evolved editing__ - IntelliSense, Peek, Hover, Diagnostics や、その他たくさんの高度な言語サポートを可能にします。

Extension の基本をひととおり学ぶための、2つのチュートリアルをご用意しました。

1. [__Hello World__](https://code.visualstudio.com/docs/extensions/example-hello-world) - 簡単な Extension を作って、フォルダ構成や manifest について理解しましょう。activation の仕組み、実行とデバッグ、ローカルへのインストールについても学びます。
1. [__Word Count__](https://code.visualstudio.com/docs/extensions/example-word-count) - ファイルタイプに応じた activation、ステータスバーの更新、テキストが変更された時の処理、ファイルを閉じた時に Extension を終了する方法について学びます。

さらに [Extensibility Principles and Patterns](https://code.visualstudio.com/docs/extensionAPI/patterns-and-principles) では、extensibility API のあちこちで使われているプログラミング・パターンについて説明しています。

<a id="_language-servers"></a>
## Language Servers

Language Server は、多くの言語において強力な編集機能をもたらす、特別な Extension です。 Language Server を使って、jump-to-definitions, autocomplete, error-checking など、多くの [language features](https://code.visualstudio.com/docs/extensionAPI/language-support) を実装する事ができます。

詳しくは [language servers](https://code.visualstudio.com/docs/extensions/example-language-server) をご覧ください。

<a id="_debug-adapter"></a>
## Debug Adapter

VS Code は標準的なデバッグの UI を備えつつ、debugger extension と "debug adapters" に従い、UI を debugger や runtime と接続します。
debug adapter は VS Code Debug Protocol を使って VS Code と通信をするためのプロセスで、すべての言語に対応します。

debugger extensions の作成についての詳細は、[こちら](https://code.visualstudio.com/docs/extensions/example-debuggers)をご覧ください。

---

実際に VS Code Extension がどんなものか見たければ、[Extension Marketplace](https://code.visualstudio.com/docs/editor/extension-gallery) で数々の便利な Extension を簡単に見る事ができます。それらをインストールして試すことで、VS Code がどのように拡張できるかのアイデアを得る事ができるでしょう。

<a id="_language-extension-guidelines"></a>
## Language Extension Guidelines

[Language Extension Guidelines](https://code.visualstudio.com/docs/extensionAPI/language-support) のページは、どんな language features を使えば良いかの参考になります。たとえば、code suggestions, actions, formatting, renaming などの language features が紹介されています。また、language server protocol を通じての実装方法や、extensibility API を直接利用する方法についても説明しています。

<a id="_themes-snippets-and-colorizers"></a>
## Themes, Snippets, and Colorizers

言語ごとのシンタックスハイライトやスニペット、カラーテーマによって、快適な編集環境を作る事ができます。TextMate 形式のファイルでこれらを設定し、VS Code でパッケージ化、再利用する事が可能です。.tmTheme, .tmSnippets, .tmLanguage などのファイルは、自作の Extension の中でもそのまま使えます。[Themes, Snippets, and Colorizers](https://code.visualstudio.com/docs/extensions/themes-snippets-colorizers) のページでは、TextMate 形式のファイルを Extension に含める方法と、themes, snippets, language colorizers を自作する方法について説明しています。

<a id="_writing-an-extension"></a>
## Writing an Extension

Yeoman [extension generator](https://code.visualstudio.com/docs/extensions/yocode) を使えば、基本的な Extension のプロジェクトを簡単に作る事ができます。まずはプロジェクトを作ってみると良いでしょう。サンプルは[こちら](https://code.visualstudio.com/docs/extensions/samples)で見る事ができます。

Extension は、TypeScript か JavaScript で書かれます。[開発、ビルド、実行、テスト、デバッグ](https://code.visualstudio.com/docs/extensions/developing-extensions)のすべてを、VS Code 上で行う事ができます。

<a id="_testing-extensions"></a>
## Testing Extensions

VS Code には、[Extension をテストする方法](https://code.visualstudio.com/docs/extensions/testing-extensions)も用意されています。VS Code API を使って自作の Extension をテストするような integration test を、実行中の VS Code インスタンス上で走らせる事が可能です。

<a id="_extension-ideas"></a>
## Extension Ideas

VS Code の機能に関する多くのアイデアは、本体の一部としてよりも Extension として実装されている方が良い場合があります。そうすればユーザは、適切な Extension を install する事で、欲しい機能を選べます。VS Code の開発者は GitHub の [vscode repository](https://github.com/Microsoft/vscode) で、`*extension-candidate` という label を使って、開発中の Extension を管理しています。もし build するのに良い Extension を探しているなら、`*extension-candidate` [issues](https://github.com/Microsoft/vscode/issues?q=is%3Aopen+is%3Aissue+label%3A*extension-candidate) を覗いてみてください。

<a id="_next-steps"></a>
## Next steps

- [Your First Extension](https://code.visualstudio.com/docs/extensions/example-hello-world) - シンプルな Hello World Extension を作ってみましょう。
- [Extension API](https://code.visualstudio.com/docs/extensionAPI/overview) - VS Code extensibility API について学びましょう。
- [Extension Examples](https://code.visualstudio.com/docs/extensions/samples) - Extension のサンプル一覧です。自分で build してみる事もできます。
