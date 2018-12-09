# Example - Hello World
([こちらのページ](https://code.visualstudio.com/docs/extensions/example-hello-world)を自分流に翻訳したものです。2018-12-09)

<a id="_your-first-extension"></a>
## Your first extension

ここでは初めての方を対象に、Visual Studio Code extension ("Hello World") を作る過程をお見せします。また、VS Code の拡張性の基本的なコンセプトについてもご説明します。

これから作る extension は、"Hello World" というテキトーな文字列を表示するコマンドを VS Code に追加するものです。後半では、VS Code editor から選択中のテキストに関する情報を取得してみます。

<a id="_prerequisites"></a>
## Prerequisites

まずは [Node.js](https://nodejs.org/ja/) をインストールして、`$PATH` を通しておきます。Node.js には extension generator をインストールするための [npm](https://www.npmjs.com/) (Node.js Package Manager) が含まれています。

<a id="_generate-a-new-extension"></a>
## Generate a new extension

とりあえず何か機能を追加したいのなら、コマンドを追加してみましょう。コマンドに callback 関数を関連付ければ、__Command Palette__ や key binding から実行する事ができます。

extension を作るための Yeoman generator があるので、これを使います。Yeoman と [Yeoman VS Code Extension generator](https://code.visualstudio.com/docs/extensions/yocode) をインストールし、真新しい extension への一歩を踏み出しましょう。
```
npm install -g yo generator-code
yo code
```
Hello World extension を作るには、__TypeScript__ extension または __JavaScript__ extension を選びます。この example では、__TypeScript__ extension を使っています。

![The command generator](https://code.visualstudio.com/assets/docs/extensions/example-hello-world/generator.png)

<a id="_running-your-extension"></a>
## Running your extension

- VS Code を起動して、`File` > `Open Folder` を選択し、生成されたフォルダを選択します。
- `F5` キーを押すか、`Debug` アイコンをクリックして `Start` を押します。
- VS Code の新規インスタンスが、特別なモード (`Extension Development Host`) で起動します。このインスタンスは、生成された extension を認識しています。
- `Ctrl+Shift+P` を押して `Hello World` というコマンドを実行します。
- これで一応、VS Code の extension を作って実行した事になります。やったね。

![Running VS Code with an extension](https://code.visualstudio.com/assets/docs/extensions/example-hello-world/running.png)

<a id="_the-structure-of-an-extension"></a>
## The structure of an extension

実行すると、extension フォルダは以下のようになります。
```
.
├── .gitignore
├── .vscode                     // VS Code integration
│   ├── launch.json
│   ├── settings.json
│   └── tasks.json
├── .vscodeignore               // files ignored when publishing extension
├── README.md
├── src
│   └── extension.ts            // the source of the extension entry point
├── test                        // test folder
│   ├── extension.test.ts       // extension.test.js, in case of JavaScript extension
│   └── index.ts                // index.js, in case of JavaScript extension
├── node_modules
│   ├── vscode                  // include vscode type definition file for extension development
│   └── typescript              // compiler for typescript (TypeScript only)
├── out                         // compilation output (TypeScript only)
│   ├── extension.js            // the extension entry point
│   ├── extension.js.map
│   └── test
│       ├── extension.test.js
│       ├── extension.test.js.map
│       ├── index.js
│       └── index.js.map
├── package.json                // extension's manifest
├── tsconfig.json               // jsconfig.json, in case of JavaScript extension
└── vsc-extension-quickstart.md // extension development quick start
```
では、これらのファイルが何のためにあるのか、見ていきましょう。

<a id="_the-extension-manifest-packagejson"></a>
### The extension manifest: `package.json`

- すべての VS Code extension には、その機能を説明するための `package.json` が必要です。
- VS Code は起動時にこのファイルを読み込み、`contributes` セクションの内容に反応するようになります。
- 詳しくは [`package.json` extension manifest reference](https://code.visualstudio.com/docs/extensionAPI/extension-manifest) をご覧ください。
- また、[`package.json` contribution points](https://code.visualstudio.com/docs/extensionAPI/extension-points) にも情報があります。

EXAMPLE TYPESCRIPT EXTENSION MANIFEST
```json
{
    "name": "myFirstExtension",
    "description": "",
    "version": "0.0.1",
    "publisher": "",
    "engines": {
        "vscode": "^1.5.0"
    },
    "categories": [
        "Other"
    ],
    "activationEvents": [
        "onCommand:extension.sayHello"
    ],
    "main": "./out/extension",
    "contributes": {
        "commands": [{
            "command": "extension.sayHello",
            "title": "Hello World"
        }]
    },
    "scripts": {
        "vscode:prepublish": "tsc -p ./",
        "compile": "tsc -watch -p ./",
        "postinstall": "node ./node_modules/vscode/bin/install",
        "test": "node ./node_modules/vscode/bin/test"
    },
    "devDependencies": {
       "typescript": "^2.0.3",
        "vscode": "^1.5.0",
        "mocha": "^2.3.3",
        "@types/node": "^6.0.40",
        "@types/mocha": "^2.2.32"
   }
}
```
> __注:__ JavaScript extension の場合、コンパイルする必要がないので、`scripts` フィールドは不要です。

上の `package.json` は、この extension について以下のことを言っています。

- `"extension.sayHello"` コマンドを実行する `"Hello world"` ラベルを、Command Palette (`Ctrl+Shift+P`) に追加します (_contributes_)。
- `"extension.sayHello"` コマンドが実行された時に、自身がロードされるようにします (_activationEvents_)。
- `"./out/extension.js"` に、_main_ JavaScript code があります。

> __注:__ VS Code は、起動時に extension のコードをロードしません。extension がどんな条件でロードされるかは、[`activationEvents`](https://code.visualstudio.com/docs/extensionAPI/activation-events) プロパティで設定されます。

<a id="_generated-code"></a>
### Generated code

生成されたコードは、`extension.ts` の中です (JaveScript extension の場合は `extension.js` の中)。
```TypeScript
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, your extension "my-first-extension" is now active!');

    // The command has been defined in the package.json file
    // Now provide the implementation of the command with  registerCommand
    // The commandId parameter must match the command field in package.json
    let disposable = vscode.commands.registerCommand('extension.sayHello', () => {
        // The code you place here will be executed every time your command is executed

        // Display a message box to the user
        vscode.window.showInformationMessage('Hello World!');
    });

    context.subscriptions.push(disposable);
}
```
- すべての extension は、その main file から `activate()` 関数を export します。この関数は、`package.json` の中のいずれかの `activationEvents` が発生した時に実行されます。ただし VS Code はこの関数を __一度しか実行しません__ 。
- もし extension が OS のリソースを使用するなら (プロセスを生成するなど)、extension はその main file から `deactivate()` 関数を export する事ができます。これは後片付けをするための関数で、VS Code の終了時にも呼び出されます。
- 今作った extension は `vscode` API を import し、コマンドを登録し、関数を `"extension.sayHello"` コマンドに関連付けます。コマンドは "Hello world" message を VS Code に表示するよう実装されています。

> __注:__ `package.json` の `contributes` セクションは、Command Palette にエントリを追加します。extension.ts/.js に書かれたコードが、`"extension.sayHello"` の実装になります。

> __注:__ TypeScript extension の場合、`out/extension.js` が生成されます。VS Code はそれをロードして実行します。

<a id="_miscellaneous-files"></a>
### Miscellaneous files

- `.vscode/launch.json` は、VS Code を Extension Development mode で起動するようにできます。さらに、`.vscode/tasks.json` で定義されているタスクの中から `preLaunchTask` を指定して、TypeScript compiler を実行する事もできます。
- `.vscode/settings.json` は、デフォルトで `out` フォルダを除外します。これを変更することで、どのファイルタイプを無視するか選ぶことができます。
- `.gitignore` - Git 用の .gitignore です。
- [`.vscodeignore`](https://code.visualstudio.com/docs/extensions/publish-extension#_advanced-usage) - Extension を publish する時に、含めたくないファイルを指定をします。
- `README.md` - この extension についての説明を書きます。
- `vsc-extension-quickstart.md` - 開発者向けの Quick Start guide です。
- `test/extension.test.ts` - この extension のための unit test を書きます。VS Code API に対して (訳者注: 原文は "against the VS Code API") テストを走らせます ([Testing Your Extension](https://code.visualstudio.com/docs/extensions/testing-extensions) をご覧ください)。

<a id="_extension-activation"></a>
## Extension activation

ここまで、extension に含まれるファイルについて見てきました。ここからは、extension をアクティベートする方法について見ていきましょう。

- extension development instance は、extension を見つけると、その中の `package.json` を読みにいきます。
- その後 `Ctrl+Shift+P` を押すと、以下のことが起こります。
- Command Palette が開いて、登録されたコマンドが表示されます。
- リストの中に `"Hello World"` コマンドがあるはずです。`package.json` で定義したからです。
- `"Hello World"` コマンドを選択すると…
- `"extension.sayHello"` が実行されます。具体的には以下のことが起こります。
    - `"onCommand:extension.sayHello"` という activation event が生成されます。
    - このイベントを `activationEvents` に定義している、すべての extension がアクティベートされます (訳者注: 以下は各 extension につき一度だけ実行される)。
        - `./out/extension.js` が JavaScript VM にロードされます。
        - VS Code は、エクスポートされた `activate()` 関数を見つけて、それを実行します。
        - `"extension.sayHello"` コマンドが登録され、コマンドに対する実装 (そのコマンドが何をするのか) が関連付けられます。
- コマンド (`"extension.sayHello"`) の実装 (であるところの関数) が実行されます。
- "Hello World" というメッセージが表示されます。

<a id="_debugging-your-extension"></a>
## Debugging your extension

コマンドの中にブレークポイントをセットして、Extension Development VS Code instance で `"Hello world"` を実行してみましょう。

![Debugging the extension](https://code.visualstudio.com/assets/docs/extensions/example-hello-world/hitbp.png)

> __注:__ TypeScript extensions の場合、VS Code は `out/extension.js` をロードして実行しますが、デバッグはオリジナルの TypeScript code 上で行うことが可能です。これは VS Code が `out/extension.js.map` を生成し、デバッグ時に参照しているためです。

> __Tip:__ コード内で、Debug Console に log を出すことができます。

Extension の開発環境について詳しく知りたければ、[こちら](https://code.visualstudio.com/docs/extensions/developing-extensions) をご覧ください。

<a id="_a-simple-change"></a>
## A simple change

`extension.ts` (または `extension.js`) を変更してみましょう。`extension.sayHello` を変更して、エディタ上で選択中のテキストの文字数を表示するようにしてみましょう。

```TypeScript
    let disposable = vscode.commands.registerCommand('extension.sayHello', () => {
        // The code you place here will be executed every time your command is executed

        let editor = vscode.window.activeTextEditor;
        if (!editor) {
            return; // No open text editor
        }

        let selection = editor.selection;
        let text = editor.document.getText(selection);

        // Display a message box to the user
        vscode.window.showInformationMessage('Selected characters: ' + text.length);
    });
```

> __Tip:__ Extension のソースコードを変更したら、__Extension Development Host__ インスタンスを再起動します。再起動するには、__Extension Development Host__ インスタンスで `Ctrl+R` (macOS: `Cmd+R`) を押すか、プライマリの VS Code インスタンスの上の方にある __Restart__ ボタンを押します。

ファイルを作成し (__File__ > __New File__)、テキストを入力して選択してください。__Hello World__ コマンドを実行すると、選択中のテキストの文字数が出力されるはずです。

![Running the modified extension](https://code.visualstudio.com/assets/docs/extensions/example-hello-world/selection-length.png)

<a id="_installing-your-extension-locally"></a>
## Installing your extension locally

ここまでで作った extension は、Extension Development instance という特殊なインスタンスでのみ実行可能です。これを VS Code のすべてのインスタンスで実行可能にするには、ローカルの extensions フォルダの中に新しくフォルダを作って、そこへコピーします。

- Windows: `%USERPROFILE%\.vscode\extensions`
- macOS/Linux: `$HOME/.vscode/extensions`

<a id="_publishing-your-extension"></a>
## Publishing your extension

Extension を公開する方法については、[こちら](https://code.visualstudio.com/docs/extensions/publish-extension)をご覧ください。

<a id="_next-steps"></a>
## Next steps

これで、ごく簡単な extension は作れるようになりました。もう少し凝った extension の例として、[Word Count Example](https://code.visualstudio.com/docs/extensions/example-word-count) では、特定の言語のみを対象とする方法や、エディタの内容が変更された時にイベントに反応する方法について、説明しています。

Extension API に関する一般的な説明については、以下のページをご覧ください。

- [Extension API Overview](https://code.visualstudio.com/docs/extensionAPI/overview) - VS Code の extensibility model 全般について。
- [API Principles and Patterns](https://code.visualstudio.com/docs/extensionAPI/patterns-and-principles) - VS Code の拡張性を支える、ルールやパターンがあります。
- [Contribution Points](https://code.visualstudio.com/docs/extensionAPI/extension-points) - VS Code の様々な contribution points について詳しく。
- [Activation Events](https://code.visualstudio.com/docs/extensionAPI/activation-events) - VS Code の activation events のリファレンス。
- [Additional Extension Examples](https://code.visualstudio.com/docs/extensions/samples) - extension のサンプルのリスト。
