class PyQmlProxy {

    // Properties

    get calculatorList() {
        return ["calculator1"]
    }

    get calculatorIndex() {
        return 0
    }

    get minimizerList() {
        return ["minimizer1"]
    }

    get minimizerIndex() {
        return 0
    }

    get amplitude() {
        return 3.5
    }

    get period() {
        return 2.0
    }

    get xShift() {
        return 0
    }

    get yShift() {
        return 0
    }

    get statusModelAsXml() {
        return "<root><item><label>Calculator</label><value>calculator1</value></item><item><label>Minimizer</label><value>minimizer1</value></item></root>"
    }

    get fitablesListAsXml() {
        return "<root><item><number>1</number><label>amplitude</label><value>3.5</value><unit></unit><error>0.0</error><fit>1</fit></item><item><number>2</number><label>period</label><value>3.141592653589793</value><unit></unit><error>0.0</error><fit>1</fit></item><item><number>3</number><label>x_shift</label><value>0.0</value><unit></unit><error>0.0</error><fit>1</fit></item><item><number>4</number><label>y_shift</label><value>0.0</value><unit></unit><error>0.0</error><fit>1</fit></item></root>"
    }

    get constraintsListAsXml() {
        return "<root><item><number>1</number><dependentName>amplitude</dependentName><relationalOperator>=</relationalOperator><value>1.0000</value><arithmeticOperator>*</arithmeticOperator><independentName>period</independentName><enabled>1</enabled></item><item><number>2</number><dependentName>amplitude</dependentName><relationalOperator>&lt;</relationalOperator><value>4.0000</value><arithmeticOperator></arithmeticOperator><independentName></independentName><enabled>1</enabled></item></root>"
    }

    get projectInfoAsJson() {
        return {"calculations":"experiments.cif","experiments":"experiments.cif","keywords":"sine, cosine, lmfit, bumps","modified":"18.09.2020, 09:24","name":"Example Project","samples":"samples.cif"}
    }

    get phasesAsXml() {
        //return "<root><item><label>Fe3O4</label><atoms><item><label>Fe1</label><type>Fe</type><x>0</x><y>0</y><z>0</z></item><item><label>Fe2</label><type>Fe</type><x>0.5</x><y>0</y><z>0</z></item><item><label>O</label><type>O</type><x>0.3421</x><y>0</y><z>0.5</z></item></atoms></item><item><label>CoO</label><atoms><item><label>Co</label><type>Co</type><x>0.5</x><y>0.25</y><z>0.5</z></item><item><label>O</label><type>O</type><x>0.75</x><y>0.75</y><z>0.75</z></item></atoms></item></root>"
        //return "<root><item><label>Sin_1</label><color>darkolivegreen</color><parameters><item><amplitude>3.2</amplitude><period>2.1</period></item></parameters></item><item><label>Sin_2</label><color>steelblue</color><parameters><item><amplitude>2.5</amplitude><period>2.7</period></item></parameters></item></root>"
        return "<root><item><label>Co2SiO4</label><color>darkolivegreen</color><crystal_system>orthorhombic</crystal_system><space_group_name>P n m a</space_group_name><space_group_setting>abc</space_group_setting><cell_length_a>10.28</cell_length_a><cell_length_b>10.28</cell_length_b><cell_length_c>10.28</cell_length_c><cell_angle_alpha>90.0</cell_angle_alpha><cell_angle_beta>90.0</cell_angle_beta><cell_angle_gamma>90.0</cell_angle_gamma><atoms><item><label>Co1</label><type>Co</type><color>coral</color><x>0.0</x><y>0.0</y><z>0.0</z><occupancy>1.0</occupancy><adp_type>Uiso</adp_type><adp_iso>0.004</adp_iso></item><item><label>Co2</label><type>Co</type><color>coral</color><x>0.279</x><y>0.279</y><z>0.279</z><occupancy>1.0</occupancy><adp_type>Uiso</adp_type><adp_iso>0.007</adp_iso></item><item><label>Si</label><type>Si</type><color>steelblue</color><x>0.094</x><y>0.094</y><z>0.094</z><occupancy>1.0</occupancy><adp_type>Uiso</adp_type><adp_iso>0.005</adp_iso></item><item><label>O1</label><type>O</type><color>darkolivegreen</color><x>0.091</x><y>0.091</y><z>0.091</z><occupancy>1.0</occupancy><adp_type>Uiso</adp_type><adp_iso>0.008</adp_iso></item><item><label>O2</label><type>O</type><color>darkolivegreen</color><x>0.448</x><y>0.448</y><z>0.448</z><occupancy>1.0</occupancy><adp_type>Uiso</adp_type><adp_iso>0.008</adp_iso></item><item><label>O3</label><type>O</type><color>darkolivegreen</color><x>0.164</x><y>0.164</y><z>0.164</z><occupancy>1.0</occupancy><adp_type>Uiso</adp_type><adp_iso>0.011</adp_iso></item></atoms></item><item><label>CoO</label><color>steelblue</color><crystal_system>cubic</crystal_system><space_group_name>F m -3 m</space_group_name><space_group_setting>1</space_group_setting><cell_length_a>3.02</cell_length_a><cell_length_b>3.02</cell_length_b><cell_length_c>3.02</cell_length_c><cell_angle_alpha>90.0</cell_angle_alpha><cell_angle_beta>90.0</cell_angle_beta><cell_angle_gamma>90.0</cell_angle_gamma><atoms><item><label>Co</label><type>Co</type><color>coral</color><x>0.0</x><y>0.0</y><z>0.0</z><occupancy>1.0</occupancy><adp_type>Uiso</adp_type><adp_iso>0.0</adp_iso></item><item><label>O</label><type>O</type><color>darkolivegreen</color><x>0.2471</x><y>0.4986</y><z>0.7497</z><occupancy>1.0</occupancy><adp_type>Uiso</adp_type><adp_iso>0.0</adp_iso></item></atoms></item></root>"
    }

    get phasesObj() {
        return [1, 2, 3]// [{"@class":"Crystal","@id":"42320499081838829392419989539816155262","@module":"easyCore.Elements.HigherLevel.Crystal","@version":"0.0.1","atoms":{"@class":"Atoms","@id":"136201934986814971809019895761751767947","@module":"easyCore.Elements.Basic.Site","@version":"0.0.1","data":[{"@class":"Site","@id":"267703642476508841055744089511086426793","@module":"easyCore.Elements.Basic.Site","@version":"0.0.1","adp":{"@class":"AtomicDisplacement","@id":"52622469657844922014787143086722223574","@module":"easyCore.Elements.Basic.AtomicDisplacement","@version":"0.0.1","adp_class":{"@class":"Isotropic","@id":"90246489117350657135401608142192911938","@module":"easyCore.Elements.Basic.AtomicDisplacement","@version":"0.0.1","Uiso":{"@class":"Parameter","@id":"143607157348918315100058166190900799669","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"The standard anisotropic atomic displacement components in angstroms squared which appear in the structure-factor term.","error":"","fixed":true,"max":null,"min":0,"name":"Uiso","units":"angstrom ** 2","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_U_iso_or_equiv.html","value":0}},"adp_type":{"@class":"Descriptor","@id":"128191497324655421295973483650864398721","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A standard code used to describe the type of atomic displacement parameters used for the site.","display_name":"adp_type","enabled":true,"name":"adp_type","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_adp_type.html","value":"Uiso"}},"fract_x":{"@class":"Parameter","@id":"28853078210649279133189683032308272570","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_x","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0},"fract_y":{"@class":"Parameter","@id":"141777612294419145197208375818284633947","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_y","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0},"fract_z":{"@class":"Parameter","@id":"268696468266720809968992131516905233639","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_z","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0},"label":{"@class":"Descriptor","@id":"31538670440731411252753970542117390918","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A unique identifier for a particular site in the crystal","display_name":"label","enabled":true,"name":"label","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_label.html","value":"Co1"},"occupancy":{"@class":"Parameter","@id":"209431791340061920621645925559051201823","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"The fraction of the atom type present at this site.","error":"","fixed":true,"max":null,"min":null,"name":"occupancy","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_occupancy.html","value":1},"specie":{"@class":"Descriptor","@id":"164694464702879996817573855279078517484","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A code to identify the atom species occupying this site.","display_name":"specie","enabled":true,"name":"specie","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_type_symbol.html","value":"Co"}},{"@class":"Site","@id":"137513826582352662977067658264683764165","@module":"easyCore.Elements.Basic.Site","@version":"0.0.1","adp":{"@class":"AtomicDisplacement","@id":"168261495335938808979945793830510080695","@module":"easyCore.Elements.Basic.AtomicDisplacement","@version":"0.0.1","adp_class":{"@class":"Isotropic","@id":"192974286058393662063776445512343784827","@module":"easyCore.Elements.Basic.AtomicDisplacement","@version":"0.0.1","Uiso":{"@class":"Parameter","@id":"307889941819773472372663647917917309550","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"The standard anisotropic atomic displacement components in angstroms squared which appear in the structure-factor term.","error":"","fixed":true,"max":null,"min":0,"name":"Uiso","units":"angstrom ** 2","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_U_iso_or_equiv.html","value":0}},"adp_type":{"@class":"Descriptor","@id":"119805347002513656543733978040496663586","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A standard code used to describe the type of atomic displacement parameters used for the site.","display_name":"adp_type","enabled":true,"name":"adp_type","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_adp_type.html","value":"Uiso"}},"fract_x":{"@class":"Parameter","@id":"325149674024670596582878568549791477132","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_x","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0.279},"fract_y":{"@class":"Parameter","@id":"312471434160030757573140672742069635580","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_y","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0.25},"fract_z":{"@class":"Parameter","@id":"154827730751900448162081930473953829343","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_z","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0.985},"label":{"@class":"Descriptor","@id":"250790175220339148369639941001366346246","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A unique identifier for a particular site in the crystal","display_name":"label","enabled":true,"name":"label","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_label.html","value":"Co2"},"occupancy":{"@class":"Parameter","@id":"111330147846836402921022646950427514988","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"The fraction of the atom type present at this site.","error":"","fixed":true,"max":null,"min":null,"name":"occupancy","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_occupancy.html","value":1},"specie":{"@class":"Descriptor","@id":"336669302119699385696903794865640506051","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A code to identify the atom species occupying this site.","display_name":"specie","enabled":true,"name":"specie","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_type_symbol.html","value":"Co"}},{"@class":"Site","@id":"287981627805717342745025381857129955525","@module":"easyCore.Elements.Basic.Site","@version":"0.0.1","adp":{"@class":"AtomicDisplacement","@id":"312544274223601679794119733112283075958","@module":"easyCore.Elements.Basic.AtomicDisplacement","@version":"0.0.1","adp_class":{"@class":"Isotropic","@id":"96282519507653006208716049093310879513","@module":"easyCore.Elements.Basic.AtomicDisplacement","@version":"0.0.1","Uiso":{"@class":"Parameter","@id":"159164221730905404632418758287563324810","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"The standard anisotropic atomic displacement components in angstroms squared which appear in the structure-factor term.","error":"","fixed":true,"max":null,"min":0,"name":"Uiso","units":"angstrom ** 2","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_U_iso_or_equiv.html","value":0}},"adp_type":{"@class":"Descriptor","@id":"339383699651201087154536544825814220830","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A standard code used to describe the type of atomic displacement parameters used for the site.","display_name":"adp_type","enabled":true,"name":"adp_type","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_adp_type.html","value":"Uiso"}},"fract_x":{"@class":"Parameter","@id":"39617895068920593924303310761174066889","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_x","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0.094},"fract_y":{"@class":"Parameter","@id":"334427154121023803184507377276399409222","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_y","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0.25},"fract_z":{"@class":"Parameter","@id":"242599593051302036810644450380932873342","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_z","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0.429},"label":{"@class":"Descriptor","@id":"267034973090720337022399758261630743246","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A unique identifier for a particular site in the crystal","display_name":"label","enabled":true,"name":"label","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_label.html","value":"Si"},"occupancy":{"@class":"Parameter","@id":"173061202640485326858390670682331989371","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"The fraction of the atom type present at this site.","error":"","fixed":true,"max":null,"min":null,"name":"occupancy","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_occupancy.html","value":1},"specie":{"@class":"Descriptor","@id":"51627627025976241001124646446736522469","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A code to identify the atom species occupying this site.","display_name":"specie","enabled":true,"name":"specie","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_type_symbol.html","value":"Si"}},{"@class":"Site","@id":"61939474463762048668755203724410154980","@module":"easyCore.Elements.Basic.Site","@version":"0.0.1","adp":{"@class":"AtomicDisplacement","@id":"259377329578428808554923090350735420165","@module":"easyCore.Elements.Basic.AtomicDisplacement","@version":"0.0.1","adp_class":{"@class":"Isotropic","@id":"211996494116178977094498097114184617983","@module":"easyCore.Elements.Basic.AtomicDisplacement","@version":"0.0.1","Uiso":{"@class":"Parameter","@id":"326375416544104898297221189416222753175","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"The standard anisotropic atomic displacement components in angstroms squared which appear in the structure-factor term.","error":"","fixed":true,"max":null,"min":0,"name":"Uiso","units":"angstrom ** 2","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_U_iso_or_equiv.html","value":0}},"adp_type":{"@class":"Descriptor","@id":"141785543925496357257732195271021562388","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A standard code used to describe the type of atomic displacement parameters used for the site.","display_name":"adp_type","enabled":true,"name":"adp_type","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_adp_type.html","value":"Uiso"}},"fract_x":{"@class":"Parameter","@id":"47804291365977028119534222998582030405","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_x","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0.091},"fract_y":{"@class":"Parameter","@id":"188267817749642772098150790733764399430","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_y","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0.25},"fract_z":{"@class":"Parameter","@id":"43566907387178408956046108954110413034","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_z","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0.771},"label":{"@class":"Descriptor","@id":"307031533217387980825487763024266123764","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A unique identifier for a particular site in the crystal","display_name":"label","enabled":true,"name":"label","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_label.html","value":"O1"},"occupancy":{"@class":"Parameter","@id":"111658462809621604932470288337216234939","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"The fraction of the atom type present at this site.","error":"","fixed":true,"max":null,"min":null,"name":"occupancy","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_occupancy.html","value":1},"specie":{"@class":"Descriptor","@id":"94963670988425835763707209085316966245","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A code to identify the atom species occupying this site.","display_name":"specie","enabled":true,"name":"specie","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_type_symbol.html","value":"O"}},{"@class":"Site","@id":"324440398993380591797824346020745526560","@module":"easyCore.Elements.Basic.Site","@version":"0.0.1","adp":{"@class":"AtomicDisplacement","@id":"59677414317928905359970569791594473182","@module":"easyCore.Elements.Basic.AtomicDisplacement","@version":"0.0.1","adp_class":{"@class":"Isotropic","@id":"197780385862934449309418720578014649748","@module":"easyCore.Elements.Basic.AtomicDisplacement","@version":"0.0.1","Uiso":{"@class":"Parameter","@id":"96665369590236085175333096210855802521","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"The standard anisotropic atomic displacement components in angstroms squared which appear in the structure-factor term.","error":"","fixed":true,"max":null,"min":0,"name":"Uiso","units":"angstrom ** 2","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_U_iso_or_equiv.html","value":0}},"adp_type":{"@class":"Descriptor","@id":"58039908065361642899688695815225329674","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A standard code used to describe the type of atomic displacement parameters used for the site.","display_name":"adp_type","enabled":true,"name":"adp_type","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_adp_type.html","value":"Uiso"}},"fract_x":{"@class":"Parameter","@id":"309651716966960700099038264595216086670","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_x","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0.448},"fract_y":{"@class":"Parameter","@id":"69261988044628523994922443527071060004","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_y","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0.25},"fract_z":{"@class":"Parameter","@id":"17607971256836676004631369645563224250","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_z","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0.217},"label":{"@class":"Descriptor","@id":"30593589331056768679652418549226585781","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A unique identifier for a particular site in the crystal","display_name":"label","enabled":true,"name":"label","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_label.html","value":"O2"},"occupancy":{"@class":"Parameter","@id":"283697600452092905857322038014692330830","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"The fraction of the atom type present at this site.","error":"","fixed":true,"max":null,"min":null,"name":"occupancy","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_occupancy.html","value":1},"specie":{"@class":"Descriptor","@id":"52036484276873593948331693971882161929","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A code to identify the atom species occupying this site.","display_name":"specie","enabled":true,"name":"specie","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_type_symbol.html","value":"O"}},{"@class":"Site","@id":"40943484346442087554483289679314045009","@module":"easyCore.Elements.Basic.Site","@version":"0.0.1","adp":{"@class":"AtomicDisplacement","@id":"91018317217938621661719130697410737303","@module":"easyCore.Elements.Basic.AtomicDisplacement","@version":"0.0.1","adp_class":{"@class":"Isotropic","@id":"302858806170020522423729292662904653734","@module":"easyCore.Elements.Basic.AtomicDisplacement","@version":"0.0.1","Uiso":{"@class":"Parameter","@id":"318621622168524324226370615166724966858","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"The standard anisotropic atomic displacement components in angstroms squared which appear in the structure-factor term.","error":"","fixed":true,"max":null,"min":0,"name":"Uiso","units":"angstrom ** 2","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_U_iso_or_equiv.html","value":0}},"adp_type":{"@class":"Descriptor","@id":"272753236285208316945504934005184038458","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A standard code used to describe the type of atomic displacement parameters used for the site.","display_name":"adp_type","enabled":true,"name":"adp_type","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_adp_type.html","value":"Uiso"}},"fract_x":{"@class":"Parameter","@id":"52264386565591557838264018430819265671","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_x","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0.164},"fract_y":{"@class":"Parameter","@id":"62768535347933825358074507378040230236","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_y","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0.032},"fract_z":{"@class":"Parameter","@id":"209586051600825470523426322155718377362","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Atom-site coordinate as fractions of the unit cell length.","error":"","fixed":true,"max":null,"min":null,"name":"fract_z","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html","value":0.28},"label":{"@class":"Descriptor","@id":"305543573000573712055958926141967956198","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A unique identifier for a particular site in the crystal","display_name":"label","enabled":true,"name":"label","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_label.html","value":"O3"},"occupancy":{"@class":"Parameter","@id":"334007121130607549323394911294786493645","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"The fraction of the atom type present at this site.","error":"","fixed":true,"max":null,"min":null,"name":"occupancy","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_occupancy.html","value":1},"specie":{"@class":"Descriptor","@id":"244533724899666014143859593816499248012","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"A code to identify the atom species occupying this site.","display_name":"specie","enabled":true,"name":"specie","units":"dimensionless","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_type_symbol.html","value":"O"}}],"name":"Atoms"},"cell":{"@class":"Cell","@id":"147075106300967923714269386923571038167","@module":"easyCore.Elements.Basic.Cell","@version":"0.0.1","angle_alpha":{"@class":"Parameter","@id":"163761455504885109201415084171339807254","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Unit-cell angle of the selected structure in degrees.","error":"","fixed":true,"max":null,"min":0,"name":"angle_alpha","units":"degree","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Icell_angle_.html","value":90},"angle_beta":{"@class":"Parameter","@id":"259569602656576887090120366881756621712","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Unit-cell angle of the selected structure in degrees.","error":"","fixed":true,"max":null,"min":0,"name":"angle_beta","units":"degree","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Icell_angle_.html","value":90},"angle_gamma":{"@class":"Parameter","@id":"92792204022917338811573472872301595514","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Unit-cell angle of the selected structure in degrees.","error":"","fixed":true,"max":null,"min":0,"name":"angle_gamma","units":"degree","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Icell_angle_.html","value":90},"length_a":{"@class":"Parameter","@id":"308592112977185350336835101214060570282","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Unit-cell length of the selected structure in angstroms.","error":"","fixed":false,"max":null,"min":0,"name":"length_a","units":"angstrom","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Icell_length_.html","value":10.28},"length_b":{"@class":"Parameter","@id":"109026685865189841549714398816263901583","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Unit-cell length of the selected structure in angstroms.","error":"","fixed":false,"max":null,"min":0,"name":"length_b","units":"angstrom","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Icell_length_.html","value":6.03},"length_c":{"@class":"Parameter","@id":"42610328425889901763403847801954301104","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"Unit-cell length of the selected structure in angstroms.","error":"","fixed":false,"max":null,"min":0,"name":"length_c","units":"angstrom","url":"https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Icell_length_.html","value":4.75}},"name":"Co2SiO4","spacegroup":{"@class":"SpaceGroup","@id":"307814036781427394045363000871867219549","@module":"easyCore.Elements.Basic.SpaceGroup","@version":"0.0.1","_space_group_HM_name":{"@class":"Descriptor","@id":"214213665652328171461375714326059514552","@module":"easyCore.Objects.Base","@version":"0.0.1","description":"","display_name":"_space_group_HM_name","enabled":true,"name":"_space_group_HM_name","units":"dimensionless","url":"","value":"P n m a"}}}]
    }

    get currentPhaseIndex() {
        return 0
    }

    get parametersCurrentIndex() {
        return 0
    }

    get currentPhaseAllSites() {
        return {"O1":[[0,0.5,0.25],[0,0.5,0.75],[0.5,0,0.25],[0.5,0,0.75],[0.5,1,0.25],[0.5,1,0.75],[1,0.5,0.25],[1,0.5,0.75]],"O2":[[0.25,0.25,0],[0.25,0.25,0.5],[0.25,0.25,1],[0.25,0.75,0],[0.25,0.75,0.5],[0.75,0.25,0],[0.75,0.25,0.5],[0.75,0.25,1],[0.75,0.75,0.5]],"Sr":[[0,0,0.25],[0,0,0.75],[0,1,0.25],[0,1,0.75],[0.5,0.5,0.25],[0.5,0.5,0.75],[1,0,0.25],[1,0,0.75],[1,1,0.25],[1,1,0.75]],"Ti":[[0,0.5,0],[0,0.5,0.5],[0,0.5,1],[0.5,0,0],[0.5,0,0.5],[0.5,0,1],[0.5,1,0],[0.5,1,0.5],[0.5,1,1],[1,0.5,0],[1,0.5,0.5],[1,0.5,1]]}
    }

    // Functions

    addLowerMeasuredSeriesRef(series) {}

    addUpperMeasuredSeriesRef(series) {}

    setCalculatedSeriesRef(series) {}

    updateCalculatedData() {}

    generateMeasuredData() {}

    startFitting() {}

    addConstraints(dependent_par_idx, operator, independent_par_idx) {}

    removeConstraintByIndex(index) {}

    toggleConstraintByIndex(index, enabled) {}

    editProjectInfoByKey(key, value) {}

    editPhase(p1, p2, p3) {}
}
