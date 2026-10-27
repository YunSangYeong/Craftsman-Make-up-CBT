import { test, expect, type Page } from '@playwright/test';

async function openMenu(page: Page) {
  await page.getByRole('button', { name: '메뉴 열기' }).click();
  await expect(page.locator('.sidebar')).toHaveClass(/open/);
  await page.waitForTimeout(250); // Wait for transform before choosing input coordinates.
}
async function inViewport(page: Page, name: string) {
  const box = await page.getByRole('button', { name, exact: true }).boundingBox();
  return !!box && box.y >= 0 && box.y + box.height <= page.viewportSize()!.height;
}
for (const size of [{ width:390,height:480 },{ width:740,height:360 },{ width:390,height:360 }]) {
  for (const input of ['wheel','touch'] as const) {
    test(`${size.width}×${size.height} ${input}: 메뉴 하단 도구와 상단 대시보드 실제 접근`, async ({page, browserName}, info) => {
      test.skip(input === 'touch' && info.project.name !== 'mobile', '터치 가능한 모바일 에뮬레이션에서 별도 검사');
      expect(browserName).toBe('chromium');
      await page.setViewportSize(size);
      await page.goto('');
      if(size.height===360 && size.width===390) await page.addStyleTag({content:'.sidebar nav button {font-size:18px; min-height:60px} .sidebar .text-button {font-size:16px}'});
      await openMenu(page);
      const sidebar = page.locator('.sidebar');
      expect(await sidebar.evaluate(el=>el.scrollHeight>el.clientHeight)).toBe(true);
      const backgroundY=await page.evaluate(()=>scrollY);
      const cdp=input==='touch'?await page.context().newCDPSession(page):null;
      async function move(down:boolean) {
        if(input==='wheel') {
          await page.mouse.move(130,size.height/2);
          await page.mouse.wheel(0,down?1000:-1000);
          await page.waitForTimeout(200);
        } else {
          const start=down?size.height-65:90, end=down?90:size.height-65;
          await cdp!.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:130,y:start}]});
          for(let i=1;i<=12;i++) {
            await cdp!.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:130,y:start+(end-start)*i/12}]});
            await page.waitForTimeout(25);
          }
          await cdp!.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
          await page.waitForTimeout(150);
        }
      }
      for(let i=0;i<8 && !(await inViewport(page,'데이터 초기화'));i++) await move(true);
      expect(await sidebar.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
      expect(await inViewport(page,'학습 기록 백업')).toBe(true);
      expect(await inViewport(page,'데이터 초기화')).toBe(true);
      // The footer actions must be reachable before Playwright auto-scroll can help.
      const download=page.waitForEvent('download');
      await page.getByRole('button',{name:'학습 기록 백업',exact:true}).click();
      expect((await download).suggestedFilename()).toBe('makeup-study-backup.json');
      await page.getByRole('button',{name:'데이터 초기화',exact:true}).click();
      await expect(page.getByRole('dialog')).toBeVisible();
      await page.getByRole('button',{name:'돌아가기',exact:true}).click();
      for(let i=0;i<8 && await sidebar.evaluate(el=>el.scrollTop)>0;i++) await move(false);
      await expect.poll(()=>sidebar.evaluate(el=>el.scrollTop)).toBe(0);
      expect(await inViewport(page,'학습 대시보드')).toBe(true);
      expect(await page.evaluate(()=>scrollY)).toBe(backgroundY);
      await page.screenshot({path:`test-results/menu-${info.project.name}-${size.width}-${size.height}-${input}.png`});
      await page.getByRole('button',{name:'학습 대시보드',exact:true}).click();
      await expect(sidebar).not.toHaveClass(/open/);
      await expect(page.getByRole('heading',{name:'미용사(메이크업) 필기 CBT',exact:true})).toBeVisible();
    });
  }
}

test('모든 주요 화면에서 상단 상시 안내 배너가 없고 저장 실패는 표시된다',async({page})=>{
  await page.goto('');
  for(const label of ['학습 대시보드','실전 모의시험','랜덤 문제풀이','오답노트','북마크','학습 통계','문제은행 관리']) {
    if(await page.getByRole('button',{name:'메뉴 열기'}).isVisible()) await openMenu(page);
    await page.getByRole('navigation').getByRole('button',{name:label,exact:true}).click();
    await expect(page.locator('.criteria-note')).toHaveCount(0);
    if(label!=='문제은행 관리') await expect(page.locator('main .notice').filter({hasText:/비공식|검증 대기|잠정|기출.*미제공|출제기준.*대조/})).toHaveCount(0);
    await expect(page.getByLabel('학습 기준')).toHaveCount(0);
  }
  await page.addInitScript(()=>{Storage.prototype.setItem=()=>{throw new DOMException('quota','QuotaExceededError')}});
  await page.reload();
  await expect(page.getByRole('alert')).toContainText('저장');
});
