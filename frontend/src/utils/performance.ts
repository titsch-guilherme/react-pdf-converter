import { onCLS, onINP, onFCP, onLCP, onTTFB, Metric } from 'web-vitals';

export interface PerformanceMetric {
  name: string;
  value: number;
  rating: 'good' | 'needs-improvement' | 'poor';
  delta: number;
  id: string;
  navigationType: string;
}

const sendToAnalytics = (metric: Metric) => {
  // In a real application, you would send this to your analytics service
  // For now, we'll just log it in development
  if (import.meta.env.DEV) {
    console.log('Web Vital:', {
      name: metric.name,
      value: metric.value,
      rating: metric.rating,
      delta: metric.delta,
      id: metric.id,
      navigationType: metric.navigationType,
    });
  }
  
  // Example: Send to Google Analytics
  // gtag('event', metric.name, {
  //   event_category: 'Web Vitals',
  //   event_label: metric.id,
  //   value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
  //   non_interaction: true,
  // });
};

export const reportWebVitals = (onPerfEntry?: (metric: PerformanceMetric) => void) => {
  const handleMetric = (metric: Metric) => {
    const perfMetric: PerformanceMetric = {
      name: metric.name,
      value: metric.value,
      rating: metric.rating,
      delta: metric.delta,
      id: metric.id,
      navigationType: metric.navigationType,
    };
    
    sendToAnalytics(metric);
    
    if (onPerfEntry && typeof onPerfEntry === 'function') {
      onPerfEntry(perfMetric);
    }
  };

  onCLS(handleMetric);
  onINP(handleMetric); // INP replaced FID in web-vitals v4+
  onFCP(handleMetric);
  onLCP(handleMetric);
  onTTFB(handleMetric);
};

export const logPerformanceMetrics = () => {
  if (import.meta.env.DEV) {
    reportWebVitals((metric) => {
      console.group(`🚀 Web Vital: ${metric.name}`);
      console.log(`Value: ${metric.value}`);
      console.log(`Rating: ${metric.rating}`);
      console.log(`Delta: ${metric.delta}`);
      console.log(`ID: ${metric.id}`);
      console.log(`Navigation Type: ${metric.navigationType}`);
      console.groupEnd();
    });
  }
};

export const measureCustomMetric = (name: string, fn: () => void | Promise<void>) => {
  const start = performance.now();
  
  const finish = () => {
    const end = performance.now();
    const duration = end - start;
    
    if (import.meta.env.DEV) {
      console.log(`⏱️ Custom Metric: ${name} took ${duration.toFixed(2)}ms`);
    }
    
    // You can send this to your analytics service
    return duration;
  };
  
  if (fn.constructor.name === 'AsyncFunction') {
    return (fn() as Promise<void>).finally(finish);
  } else {
    fn();
    return finish();
  }
};

export const observeElementPerformance = (element: Element, name: string) => {
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const loadTime = performance.now();
          if (import.meta.env.DEV) {
            console.log(`👁️ Element "${name}" became visible at ${loadTime.toFixed(2)}ms`);
          }
          observer.unobserve(element);
        }
      });
    });
    
    observer.observe(element);
  }
};

// Performance budget thresholds (in milliseconds)
export const PERFORMANCE_THRESHOLDS = {
  FCP: { good: 1800, poor: 3000 }, // First Contentful Paint
  LCP: { good: 2500, poor: 4000 }, // Largest Contentful Paint
  INP: { good: 200, poor: 500 },   // Interaction to Next Paint (replaced FID)
  CLS: { good: 0.1, poor: 0.25 },  // Cumulative Layout Shift
  TTFB: { good: 800, poor: 1800 }, // Time to First Byte
} as const;

export const checkPerformanceBudget = (metrics: PerformanceMetric[]) => {
  const results = metrics.map((metric) => {
    const threshold = PERFORMANCE_THRESHOLDS[metric.name as keyof typeof PERFORMANCE_THRESHOLDS];
    if (!threshold) return { ...metric, withinBudget: true };
    
    const withinBudget = metric.value <= threshold.good;
    return { ...metric, withinBudget, threshold };
  });
  
  const failedMetrics = results.filter(r => !r.withinBudget);
  
  if (failedMetrics.length > 0 && import.meta.env.DEV) {
    console.warn('⚠️ Performance budget exceeded:', failedMetrics);
  }
  
  return results;
};