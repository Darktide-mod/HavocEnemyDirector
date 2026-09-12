// Run the installed Darktide extension's actual archive-routing functions offline.
const fs = require('fs');
const vm = require('vm');
const path = require('path').win32;
const source = fs.readFileSync(process.argv[2], 'utf8');
const start = source.indexOf('function testSupportedContent(files, gameId)');
const end = source.indexOf('async function install_mod_load_order_file_maker', start);
if (start < 0 || end < 0) throw Error('Installed Vortex extension changed; review its installer.');
const sandbox = {path, GAME_ID: 'warhammer40kdarktide', MOD_FILE_EXT: '.mod', BAT_FILE_EXT: '.bat', updating_mod: false, mod_install_name: 'release check', api_warning: (...args) => {throw Error('Unexpected Vortex warning: ' + JSON.stringify(args));}};
vm.createContext(sandbox);
vm.runInContext(source.slice(start, end), sandbox);
const mods = JSON.parse(fs.readFileSync(0, 'utf8'));
(async () => {
    let count = 0;
    for (const mod of mods) {
        const files = mod.files.map(p => p.replaceAll('/', '\\'));
        if (!(await sandbox.testSupportedContent(files, 'warhammer40kdarktide')).supported) throw Error(mod.name + ' unsupported');
        const {instructions} = await sandbox.installContent(files);
        if (instructions.length !== files.length) throw Error('Installer omitted files: ' + mod.name);
        for (const instruction of instructions) {
            if (instruction.type !== 'copy' || instruction.destination !== path.join('mods', instruction.source)) throw Error('Unexpected installation path: ' + JSON.stringify(instruction));
            count++;
        }
    }
    process.stdout.write(JSON.stringify({status: 'passed', mods: mods.length, installed_paths: count, unexpected_root_install_warnings: 0}));
})().catch(error => {console.error(error);process.exitCode = 1;});
