# React開発で、オブジェクトの型を、どう定義するのが効率的なのかを調べる

ReactをTypeScriptで開発したい、と思ったときに、型を、どうやって定義したら良いのか意外と自明ではなかったので
調べてみた。

## 例

例えば、以下のようなER図で表されるClientとDealというエンティティのCRUDアプリを考えてみる。

``` mermaid
erDiagram
  Client ||--o{ Deal : contains
  Client {
    int id
    string name
  }
  Deal {
    int id
    string name
    int clientId
  }
```

すごいシンプルに

``` typescript
type Client = {
    id: number,
    name: string
};
type Deal = {
    id: number,
    name: string,
    clientId: number
}
```

というような型を、まずは定義することになる。
しかし、実際にCRUDの機能を考えると、型はこれだけでは全く足らないことが分かる。

## 新規作成時の問題

例えば、Dealの新規作成を考える。Dealを作成するにはnameとclientIdが必要なので、それぞれを入力するための
何かしらの入力要素が用意される。Reactでは、`useState`を使って、これら入力要素の内容をstateと同期することが
一般的である。

このstateの型をどうすれば良いか。DBのスキーマから自然に導かれる型においては、
Dealの全てのプロパティはnot nullである。
一方で、今、まさに定義しようとしているDealオブジェクトには、まだ、名前が記入されてないかもしれない。
そもそも、idはDBで自動発番したいので、フロント側で情報を入力している間には決まりようがない 🙃

## 一覧時の問題

Clientの一覧画面を考えてみる。Clientには、0個以上複数のDealが紐付いているので、こいつらも一緒に表示したいとしよう。
個々のClientごとに、対応するDealを問い合わせるのはN+1問題なので、API側に、Dealも含めてClientの一覧を返すような
エンドポイントを用意することになるだろう。この返り値の型は、どうすべきだろうか。
上のClient型の定義には、`deals: Deal[]`のようなプロパティはない 🤔

## まとめ

上のような状況に対応するためには、基本となる型(ClientやDeal)をもとにして、一部のプロパティをOptionalにしたり、新しいプロパティを追加したりできるようにしたい。TypeScriptには、Omit、Pick、Partialなどなど、そういったニーズに
対応する型を操作して別の型を作る機能がある。
Reactで、典型的なアプリを作る場合に、これらをどう組み合わせるのが効果的なのかを調べた・・というのがこのレポジトリの
意図である。
