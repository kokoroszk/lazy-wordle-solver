import { Char, wordList, frequency, letters_ord_high_frequency } from "./utils";

// 重複のない20個のアルファベットを含む単語セット。可能な限り頻出の英字。
export const trainingAnswers = ["rynds", "mulct", "bigha", "kopje"];

const fixed: Char[] = ["", "", "", "", ""];
const included: Char[] = [];
const excluded: Set<string> = new Set();
const checked: Set<string> = new Set();

// 指定した文字種で作れる5文字の文字列を生成する
const comb = (
  letters: Char[],
  fixed: Char[],
  uniq: boolean = false, // 一度使用した文字種の再利用を許可するか
  buf: Char[] = [],
  result: Char[][] = []
): Char[][] => {
  if (buf.length == 5) {
    result.push(buf);
    return result;
  }

  if (fixed[buf.length] != "") {
    return comb(letters, fixed, uniq, buf.concat(fixed[buf.length]), result);
  }

  for (let l of letters) {
    let _letters = letters.concat();
    if (uniq) {
      const i = _letters.indexOf(l);
      _letters.splice(i, 1);
    }
    comb(_letters, fixed, uniq, buf.concat(l), result);
  }
  return result;
};

// 可能な5文字の文字列を生成して、辞書に存在するもののみ返却する
const generateWords = (letters: Char[], fixed: Char[], excluded: Set<string>) =>
  comb(
    letters.filter((l) => !excluded.has(l)),
    fixed
  ).filter((word) => wordList.includes(word.join("")));

// 位置・個数が確定した文字から、あり得る組み合わせ(穴あき)を生成する
const makeCandidate = (fixed: Char[], included: Char[]) => {
  const fixedCnt = fixed.reduce((acc, d) => acc + (d === "" ? 0 : 1), 0);
  const letters = [].concat(included);
  for (let i = included.length + fixedCnt; i < 5; i++) letters.push("");
  return Array.from(
    new Set(comb(letters, fixed, true).map((w) => w.join(",")))
  ).map((w) => w.split(","));
};

// 位置・個数が確定した文字の全組み合わせを元に、辞書に存在する単語を取得する
const generateAnswers = (
  fixed: Char[],
  included: Char[],
  excluded: Set<string>,
  checked: Set<string>
) =>
  makeCandidate(fixed, included)
    .flatMap((c) =>
      generateWords(
        letters_ord_high_frequency.split("") as any,
        c as any,
        excluded
      )
    )
    .filter((arrword) => !checked.has(arrword.join("")));

// 出現率の高い単語を多く含む単語を選択する
// 選び方変えた方がよい...。
type ChoiseAcc = [Char[], number];
const choise = (answers: Char[][]) => {
  const c: ChoiseAcc = answers.reduce(
    (acc, arrword) => {
      const [word, score] = acc;
      const currScore = arrword.map(frequency).reduce((p, c) => p + c);
      return score > currScore ? acc : [arrword, currScore];
    },
    [["", "", "", "", ""], 0]
  );
  return c[0];
};

export const nextWord = () =>
  choise(generateAnswers(fixed, included, excluded, checked));

// wordleの判定結果を処理する
// fixed, included, excluded, checkedを書き換える
export type Evaluation = "correct" | "absent" | "present";
export const checkResult = (ans: Char[], ret: Evaluation[]) => {
  checked.add(ans.join(""));
  if (ret.every((r) => r === "correct")) return true;

  // 同一文字が複数存在するwordのpresent判定のため個数を数える
  const wbuf = {};
  ans.forEach((c) => {
    const n = wbuf[c] || 0;
    wbuf[c] = n + 1;
  });

  // correct判定
  const correctIdx = new Set<number>();
  for (let i = 0; i < 5; i++) {
    if (ret[i] === "correct") {
      fixed[i] = ans[i];
      correctIdx.add(i);
      if (ans[i] in included) {
        const idx = included.indexOf(ans[i]);
        included.splice(idx, 1);
      }
    }
  }

  // present判定
  const ybuf: any = {};
  for (let i = 0; i < 5; i++) {
    if (ret[i] === "present") {
      const n = ybuf[ans[i]] || 0;
      ybuf[ans[i]] = n + 1;
    }
  }
  for (let [k, v] of Object.entries(ybuf)) {
    const num = included.filter((i) => i === k).length;
    // あり得る個数分がincludedに追加されたら、excludedに追加してよい
    // fixed + includedで候補を生成してから、excluded以外の英字で単語を生成するため
    for (let i = num; i < v; i++) included.push(k as Char);
    if (wbuf[k] > v) excluded.add(k);
  }

  ans
    .filter((a, idx) => !correctIdx.has(idx))
    .filter((a) => included.indexOf(a) === -1)
    .forEach((a) => excluded.add(a));
  return false;
};
