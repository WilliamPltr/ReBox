module.exports = {
  mode: 'jit', // Active le mode JIT
  content: [
    './templates/**/*.html',   // Tous les fichiers HTML dans le dossier templates
    './core/templates/**/*.html', // Si tes templates Django sont dans un sous-dossier
    './static/**/*.js',        // Tous les fichiers JavaScript dans le dossier static
    './static/**/*.css',       // Ajout pour CSS
  ],
  theme: {
    extend: {
      // Ajoutez votre ligne ici dans "extend"
      borderRadius: {
        '1.5xl': '1.125rem', // Entre "xl" (1rem) et "2xl" (1.5rem)
      },
    },
  },
  daisyui: {
    themes: [
      {
        opack: {
          primary: '#0077b6', // Bleu stylé
          secondary: '#ffdd99', // Beige doré
          accent: '#fffefb', // Blanc cassé
          neutral: '#3d4451', // Couleur neutre supplémentaire
          'base-100': '#fffefb', // Fond blanc cassé
          info: '#3abff8',
          success: '#36d399',
          warning: '#fbbd23',
          error: '#f87272',
        },
      },
    ],
  },
  plugins: [require('daisyui')],
};
