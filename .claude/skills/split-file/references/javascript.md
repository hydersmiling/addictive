# Splitting a JavaScript or TypeScript module safely

## Use a folder with an index that re-exports
Before: `src/utils.ts` (1,200 lines). After:
```
src/utils/
  index.ts       // re-exports the public API
  dates.ts
  money.ts
  strings.ts
```
`src/utils/index.ts`:
```ts
export { formatDate, parseDate } from "./dates";
export { formatMoney, type Money } from "./money";
export * from "./strings";
```
`import { formatDate } from "./utils"` keeps working, because a folder import resolves to
its `index` file in Node-style resolution, TypeScript and common bundlers.

## Or keep the old file as a barrel
If other tools reference the file path itself, keep `utils.ts` and make it re-export from
the new files: `export * from "./utils/dates";`

## Watch out for
- **Default exports:** re-export them explicitly: `export { default } from "./dates";` or
  `export { default as dates } from "./dates";`. `export *` does not include defaults.
- **Type-only exports** in TypeScript with `isolatedModules`: use `export type { Money }`.
- **Circular imports:** move shared types or constants into their own file rather than
  importing two new modules from each other.
- **Side effects at import time** (polyfills, registrations): keep them in one module that
  is still imported where it was before, or behaviour changes silently.
- **ES modules in Node without a bundler:** imports need the file extension
  (`"./dates.js"`) and folder imports do not resolve to `index.js`; keep the old file as a
  barrel in that case.
- **Tree shaking:** a barrel with many `export *` lines can pull in more code than needed;
  prefer named re-exports for large libraries.
