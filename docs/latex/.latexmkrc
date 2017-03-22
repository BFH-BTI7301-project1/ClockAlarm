add_cus_dep( 'glo', 'gls', 0, 'makeglo2gls' );
sub makeglo2gls {
    system("makeindex -s \"$_[0].ist\" -t \"$_[0].glg\" -o \"$_[0].gls\" \"$_[0].glo\"" );
}

add_cus_dep( 'acn', 'acr', 0, 'makeacr2acn' );
sub makeacr2acn {
    system( "makeindex -s \"$_[0].ist\" -t \"$_[0].alg\" -o \"$_[0].acr\" \"$_[0].acn\"" );
}

push @generated_exts, 'glo', 'gls', 'glg';
push @generated_exts, 'acn', 'acr', 'alg';
$clean_ext .= ' %R.ist %R.xdy';