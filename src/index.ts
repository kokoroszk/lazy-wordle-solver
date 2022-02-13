import { argv } from "process";
import { checkResult, Evaluation, trainingAnswers, nextWord } from "./solver";
import puppeteer from "puppeteer";

const sleep = (millis) => new Promise((resolve) => setTimeout(resolve, millis));
const ENTER = "↵";
const utils = (page: puppeteer.Page) => ({
  async send(keys) {
    for (let i = 0; i < keys.length; i++)
      await page.click(`pierce/button[data-key="${keys[i]}"]`);
    await page.click(`pierce/button[data-key="${ENTER}"]`);
  },
  async judge(turn: number): Promise<Evaluation[]> {
    const gameRow = (await page.$$("pierce/game-row")).at(turn - 1);
    const gameTile = await gameRow.$$("pierce/game-tile");
    return Promise.all(
      gameTile.map((n) => n.evaluate((el) => el.getAttribute("evaluation")))
    ) as any;
  },
});

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: argv.filter((v) => v.startsWith("--")),
  });
  const page = await browser.newPage();
  const u = utils(page);

  try {
    await page.goto("https://www.nytimes.com/games/wordle/index.html");
    await page.click("pierce/.close-icon");
    await sleep(1000);

    let turn = 0;
    for (const answer of trainingAnswers) {
      turn++;
      await u.send(answer.split(""));
      await sleep(1800);
      const j = await u.judge(turn);
      const isCorrect = checkResult(answer.split("") as any, j);
      if (isCorrect) break;
    }

    for (; turn < 6; ) {
      turn++;
      const ans = nextWord();
      await u.send(ans);
      await sleep(1800);
      const j = await u.judge(turn);
      const isCorrect = checkResult(ans, j);
      if (isCorrect) break;
    }

    await sleep(4000);
    await page.screenshot({ path: "./image.png" });
  } catch (err) {
    console.log(err);
  } finally {
    await browser.close();
  }
})();
