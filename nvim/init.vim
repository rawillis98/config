call plug#begin('~/.local/share/nvim/plugged')

Plug 'vim-airline/vim-airline'
Plug 'davidhalter/jedi-vim'
Plug 'scrooloose/nerdcommenter'
Plug 'ericbn/vim-relativize'
Plug 'scrooloose/nerdtree'
Plug 'majutsushi/tagbar'
Plug 'nvie/vim-flake8'
Plug 'tpope/vim-surround'
Plug 'jiangmiao/auto-pairs'
Plug 'airblade/vim-gitgutter'

call plug#end()

set number relativenumber
set shiftwidth=0 tabstop=4
set colorcolumn=80

autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() == 0 && !exists("s:std_in") | NERDTree | endif

map <C-n> :NERDTreeToggle<CR>
imap <C-l> <Esc>
map <F8> :TagbarToggle<CR>
nnoremap <buffer> <F9> :exec '!python' shellescape(@%, 1)<cr>
nnoremap <F10> :exec '!python -m pytest'<cr>


