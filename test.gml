graph [
directed 1
node [ id 0 label "0" graphics [ fill	"#00FF7F" w 40 h 30 x 80 y 70 type "ellipse" ]]
node [ id 1 label "1" graphics [ fill	"#FF3300" w 40 h 30 x 62 y 171 type "ellipse" ]]
node [ id 2 label "2" graphics [ fill	"#FF3300" w 40 h 30 x 180 y 138 type "ellipse" ]]
edge [ source 0 target 1  graphics [ fill	"#000000" targetArrow "delta" ]]
edge [ source 1 target 2  graphics [ fill	"#000000" targetArrow "delta" ]]
edge [ source 2 target 1  graphics [ fill	"#000000" targetArrow "delta" ]]
]
