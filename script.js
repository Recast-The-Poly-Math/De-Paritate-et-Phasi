const power = document.querySelector('#power');
const output = document.querySelector('#power-output');
const labels = ['#power-label', '#power-label-2', '#power-label-3'].map((id) => document.querySelector(id));
const expansion = document.querySelector('#expansion');
const verdict = document.querySelector('#verdict');
const superscripts = ['⁰','¹','²','³','⁴','⁵','⁶','⁷','⁸','⁹'];
const sup = (n) => String(n).split('').map((d) => superscripts[Number(d)]).join('');
const choose = (n,k) => { let r=1; for(let i=1;i<=k;i++) r=r*(n-i+1)/i; return r; };
const term = (n,k) => {
  const coefficient = choose(n,k);
  const sign = k === 0 ? '' : (k % 2 ? ' − ' : ' + ');
  const cPower = n-k;
  const bPower = k;
  const parts=[];
  if(coefficient!==1) parts.push(coefficient);
  if(cPower>0) parts.push('c'+(cPower===1?'':sup(cPower)));
  if(bPower>0) parts.push('b'+(bPower===1?'':sup(bPower)));
  return sign + (parts.join('') || '1');
};
function updateExplorer(){
  const n=Number(power.value);
  output.value=n;
  labels.forEach((label)=>label.textContent=n);
  let numerator='';
  for(let k=0;k<=n;k++) numerator+=term(n,k);
  expansion.textContent=`(${numerator}) / a${sup(n)} = 1`;
  verdict.innerHTML=n%2
    ? '<strong>Odd exponent:</strong> the converse retains the sign and recovers c = a + b.'
    : '<strong>Even exponent:</strong> the forward law holds, but the converse permits c = b ± a.';
}
power.addEventListener('input',updateExplorer);
updateExplorer();
