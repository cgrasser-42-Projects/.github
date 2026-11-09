// Dumps the logos used by the README from the Simple Icons package (simpleicons.org, CC0)
// into icons.json, read by build_profile.py.
const si = require('simple-icons');
const slugs = ['42', 'git', 'docker', 'rust', 'cplusplus', 'qt', 'c', 'linux', 'github', 'discord', 'gmail'];
const out = {};
for (const slug of slugs) {
  const icon = Object.values(si).find((i) => i && i.slug === slug);
  if (icon) out[slug] = { title: icon.title, hex: '#' + icon.hex, path: icon.path };
}
require('fs').writeFileSync(require('path').join(__dirname, 'icons.json'), JSON.stringify(out));
console.log('icons:', Object.keys(out).join(', '));
