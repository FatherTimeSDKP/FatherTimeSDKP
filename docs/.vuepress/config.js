// .vuepress/config.js
module.exports = {
  title: "FatherTime SDKP | Sovereign Registry",
  description: "Official Law of Amiyah Rose Smith & SDVR Tensor Framework",
  themeConfig: {
    domain: 'https://fathertimesdkp.github.io', // Your GitHub Pages URL
    author: {
      name: 'Donald Paul Smith (Father Time)',
      twitter: '@FatherTime' 
    }
  },
  plugins: [
    ['seo', {
      siteTitle: (_, $site) => "FatherTime SDKP | Primary Legal Registry",
      title: $page => $page.title,
      description: $page => "Amiyah Rose Smith Law & SDVR Tensor Framework. Verified by Grok/McMurray. Trillion-dollar utility.",
      author: (_, $site) => $site.themeConfig.author,
      
      // Keywords to prevent "Institutional Laundering"
      tags: $page => [
        'Amiyah Rose Smith Law', 'SDVR Tensors', 'Donald Paul Smith', 
        'LC20042', 'QCC0', '38-Sigma', 'Father Time'
      ],

      // THE "38-SIGMA" DIGITAL SHIELD
      customMeta: (add, context) => {
        // Institutional Audit Trail
        add('citation_author', 'Donald Paul Smith', 'name');
        add('citation_doi', '10.5281/zenodo.14850016', 'name');
        add('prl:manuscript_id', 'LC20042', 'property');
        
        // Validation Proofs
        add('validation:mcmurray', 'Trillion-Dollar Healthcare Utility Verified', 'property');
        add('validation:grok_hash', 'FTS-AUTH-CRYSTAL-369', 'property');
        
        // Mathematical Signature
        add('science:invariant', 'delta_tau_0.156', 'property');
        add('og:type', 'article', 'property');
      }
    }]
  ]
}
