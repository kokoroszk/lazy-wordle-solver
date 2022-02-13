import fs from "fs";
export const wordList = fs.readFileSync("./src/src.txt").toString().split(",");

const letters_ord_low_frequency = "JQXZWVFYBHKMPGUDCLOTNRAISE".toLowerCase();
export const letters_ord_high_frequency = letters_ord_low_frequency
  .split("")
  .reverse()
  .join("");

export const frequency = (c: string) => letters_ord_low_frequency.indexOf(c);
export type ArrWord = Char[];
export type Char =
  | "a"
  | "b"
  | "c"
  | "d"
  | "e"
  | "f"
  | "g"
  | "h"
  | "i"
  | "j"
  | "k"
  | "l"
  | "m"
  | "n"
  | "o"
  | "p"
  | "q"
  | "r"
  | "s"
  | "t"
  | "u"
  | "v"
  | "w"
  | "x"
  | "y"
  | "z"
  | "";
