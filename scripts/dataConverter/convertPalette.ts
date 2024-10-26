import * as fs from "fs";
import chroma from "chroma-js";

/**
 * @param hex
 * @returns [l, c, h] 各値は0-1の範囲で、小数点以下第3位
 */
const convertRgbToOklch = (hex: string): number[] => {
  const [l, c, h] = chroma(hex).oklch();
  return [l, c, h / 360].map((value) => Math.round(value * 1000) / 1000);
};

/**
 * RGBパレットをOklchパレットに変換する
 * また、hueの値で順序をソートする
 */
const convertPaletteList = (rgbPalette: string[][]) => {
  const convertedPaletteList = rgbPalette
    .map((palette: string[]) => palette.map(convertRgbToOklch))
    .filter((palette) =>
      palette.every((lch) => lch.every((value) => !isNaN(value))),
    );

  const sortedPaletteList = convertedPaletteList
    .map((palette) => palette.sort((a, b) => a[2] - b[2]))
    .sort((a, b) => a[0][2] - b[0][2]);
  return sortedPaletteList;
};

const rgbPalettePath = "../../data/raw/rgbPalette.json";
const rgbPaletteList = JSON.parse(fs.readFileSync(rgbPalettePath, "utf-8"));

const outputFilePath = "../../data/processed/oklchPalette.json";
fs.writeFileSync(
  outputFilePath,
  JSON.stringify(convertPaletteList(rgbPaletteList), null, 2),
);

console.log(`変換完了。ファイルに保存されました: ${outputFilePath}`);
