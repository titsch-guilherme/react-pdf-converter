import { theme } from './theme';

describe('Theme Configuration', () => {
  test('has correct primary colors', () => {
    expect(theme.palette.primary.main).toBe('#1976d2');
    expect(theme.palette.primary.light).toBe('#42a5f5');
    expect(theme.palette.primary.dark).toBe('#1565c0');
    expect(theme.palette.primary.contrastText).toBe('#ffffff');
  });

  test('has correct secondary colors', () => {
    expect(theme.palette.secondary.main).toBe('#dc004e');
    expect(theme.palette.secondary.light).toBe('#ff5983');
    expect(theme.palette.secondary.dark).toBe('#9a0036');
    expect(theme.palette.secondary.contrastText).toBe('#ffffff');
  });

  test('has correct background colors', () => {
    expect(theme.palette.background.default).toBe('#f5f5f5');
    expect(theme.palette.background.paper).toBe('#ffffff');
  });

  test('has correct text colors', () => {
    expect(theme.palette.text.primary).toBe('#333333');
    expect(theme.palette.text.secondary).toBe('#666666');
  });

  test('has correct typography settings', () => {
    expect(theme.typography.fontFamily).toBe('"Roboto", "Helvetica", "Arial", sans-serif');
    expect(theme.typography.h1.fontSize).toBe('2.5rem');
    expect(theme.typography.h1.fontWeight).toBe(600);
    expect(theme.typography.button.textTransform).toBe('none');
  });

  test('has correct breakpoints', () => {
    expect(theme.breakpoints.values.xs).toBe(0);
    expect(theme.breakpoints.values.sm).toBe(600);
    expect(theme.breakpoints.values.md).toBe(900);
    expect(theme.breakpoints.values.lg).toBe(1200);
    expect(theme.breakpoints.values.xl).toBe(1536);
  });

  test('has correct spacing and shape', () => {
    expect(theme.spacing(1)).toBe('8px'); // MUI v5+ returns string with px
    expect(theme.shape.borderRadius).toBe(8);
  });

  test('has custom status colors', () => {
    expect(theme.status.danger).toBe('#f44336');
  });

  test('has component overrides', () => {
    expect(theme.components?.MuiButton?.styleOverrides?.root).toBeDefined();
    expect(theme.components?.MuiCard?.styleOverrides?.root).toBeDefined();
    expect(theme.components?.MuiPaper?.styleOverrides?.root).toBeDefined();
  });
});