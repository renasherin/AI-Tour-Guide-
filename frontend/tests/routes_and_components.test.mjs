/**
 * Frontend Route and Component Smoke Tests using Node.js Test Runner.
 */

import { test, describe } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SRC_DIR = path.resolve(__dirname, "../src");

describe("Incredible Journeys Frontend Architecture Smoke Tests", () => {
  test("All required page routes exist in App Router", () => {
    const requiredRoutes = [
      "app/page.tsx",
      "app/explore/page.tsx",
      "app/destinations/[slug]/page.tsx",
      "app/guide/page.tsx",
      "app/about/page.tsx",
      "app/layout.tsx",
    ];

    for (const route of requiredRoutes) {
      const fullPath = path.join(SRC_DIR, route);
      assert.ok(fs.existsSync(fullPath), `Route file must exist: ${route}`);
      const content = fs.readFileSync(fullPath, "utf-8");
      assert.ok(content.length > 100, `Route file should have non-trivial code: ${route}`);
    }
  });

  test("UI and Motion components exist with complete exports", () => {
    const requiredComponents = [
      "components/ui/Navbar.tsx",
      "components/ui/Footer.tsx",
      "components/ui/DestinationCard.tsx",
      "components/map/DestinationMap.tsx",
      "components/chat/ChatMessageItem.tsx",
      "components/chat/GlobalChatDrawer.tsx",
      "components/motion/MotionWrapper.tsx",
    ];

    for (const comp of requiredComponents) {
      const fullPath = path.join(SRC_DIR, comp);
      assert.ok(fs.existsSync(fullPath), `Component file must exist: ${comp}`);
      const content = fs.readFileSync(fullPath, "utf-8");
      assert.ok(content.includes("export"), `Component must export elements: ${comp}`);
    }
  });

  test("Data models and API client contracts are well-defined", () => {
    const apiPath = path.join(SRC_DIR, "lib/api.ts");
    const typesPath = path.join(SRC_DIR, "lib/types.ts");
    const imagesPath = path.join(SRC_DIR, "lib/images.ts");

    assert.ok(fs.existsSync(apiPath), "api.ts must exist");
    assert.ok(fs.existsSync(typesPath), "types.ts must exist");
    assert.ok(fs.existsSync(imagesPath), "images.ts must exist");

    const apiContent = fs.readFileSync(apiPath, "utf-8");
    assert.ok(apiContent.includes("fetchDestinations"), "Must implement fetchDestinations");
    assert.ok(apiContent.includes("streamRAGChat"), "Must implement streamRAGChat");
    assert.ok(apiContent.includes("fetchRegions"), "Must implement fetchRegions");

    const typesContent = fs.readFileSync(typesPath, "utf-8");
    assert.ok(typesContent.includes("Destination"), "Must define Destination interface");
    assert.ok(typesContent.includes("SourceCitation"), "Must define SourceCitation interface");
    assert.ok(typesContent.includes("RegionDivision"), "Must define RegionDivision interface");
  });

  test("Editorial Design Tokens conform to Anti-Slop Directive", () => {
    const tailwindPath = path.resolve(__dirname, "../tailwind.config.ts");
    assert.ok(fs.existsSync(tailwindPath), "tailwind.config.ts must exist");

    const content = fs.readFileSync(tailwindPath, "utf-8");
    // Verify anti-slop color palette
    assert.ok(content.includes("#C85A32") || content.includes("terracotta"), "Must include Terracotta");
    assert.ok(content.includes("#D9822B") || content.includes("saffron"), "Must include Saffron");
    assert.ok(content.includes("#1E3A2F") || content.includes("viridian"), "Must include Viridian");
    assert.ok(content.includes("#FAF8F5") || content.includes("ivory"), "Must include Warm Ivory");
    assert.ok(content.includes("#0F141C") || content.includes("obsidian"), "Must include Obsidian");
  });
});
