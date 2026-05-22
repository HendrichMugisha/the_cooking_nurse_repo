module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './static/**/*.js',
  ],
  theme: {
    extend: {
      "colors": {
        "primary": "#0F5B30",
        "accent": "#E31818",
        "tertiary": "#C69C08",
        
        "surface": "#ffffff",
        "surface-container": "#f8f9fa",
        "surface-container-low": "#f1f3f5",
        "surface-container-lowest": "#ffffff",
        "surface-container-high": "#e9ecef",
        
        "on-surface": "#212529",
        "on-surface-variant": "#495057",
        
        "outline-variant": "#dee2e6",
        
        "on-primary": "#ffffff",
        "on-error-container": "#E31818",
        "error-container": "#ffe6e6",
      },
      "fontFamily": {
        "headline-sm": ["Outfit", "sans-serif"],
        "body-lg": ["Inter", "sans-serif"],
        "headline-md": ["Outfit", "sans-serif"],
        "display-lg-mobile": ["Outfit", "sans-serif"],
        "label-sm": ["Inter", "sans-serif"],
        "body-md": ["Inter", "sans-serif"],
        "display-lg": ["Outfit", "sans-serif"],
        "label-md": ["Inter", "sans-serif"],
        "headline-lg": ["Outfit", "sans-serif"]
      },
      "fontSize": {
        "headline-sm": ["24px", {"lineHeight": "32px", "fontWeight": "700"}],
        "body-lg": ["18px", {"lineHeight": "28px", "fontWeight": "400"}],
        "headline-md": ["32px", {"lineHeight": "40px", "fontWeight": "800"}],
        "display-lg-mobile": ["40px", {"lineHeight": "48px", "letterSpacing": "-0.02em", "fontWeight": "800"}],
        "label-sm": ["12px", {"lineHeight": "16px", "fontWeight": "600"}],
        "body-md": ["16px", {"lineHeight": "24px", "fontWeight": "400"}],
        "display-lg": ["56px", {"lineHeight": "64px", "letterSpacing": "-0.03em", "fontWeight": "900"}],
        "label-md": ["14px", {"lineHeight": "20px", "letterSpacing": "0.05em", "fontWeight": "700"}],
        "headline-lg": ["36px", {"lineHeight": "44px", "fontWeight": "800"}]
      },
      "boxShadow": {
        'level-1': '0 4px 6px -1px rgba(15, 91, 48, 0.05), 0 2px 4px -1px rgba(15, 91, 48, 0.03)',
        'level-2': '0 10px 15px -3px rgba(15, 91, 48, 0.08), 0 4px 6px -2px rgba(15, 91, 48, 0.04)',
      },
      "spacing": {
        "gutter": "24px",
        "margin-mobile": "16px",
        "base": "8px",
        "margin-desktop": "48px",
        "container-max": "1280px"
      },
    }
  },
  plugins: [],
}
