from BusinessObjectFactory import BusinessObjectFactory

input_text = """
Псалом 1

1 Блаже́н муж, и́же не и́де на сове́т нечести́вых и на пути́ гре́шных не ста, и на седа́лищи губи́телей не се́де,
2 но в зако́не Госпо́дни во́ля eго́, и в зако́не Его́ поучи́тся день и нощь.
3 И бу́дет я́ко дре́во насажде́нное при исхо́дищих вод, е́же плод свой даст во вре́мя свое́, и лист eго́ не отпаде́т, и вся, ели́ка а́ще твори́т, успе́ет.
4 Не та́ко нечести́вии, не та́ко, но я́ко прах, eго́же возмета́ет ветр от лица́ земли́.
5 Сего́ ра́ди не воскре́снут нечести́вии на суд, ниже́ гре́шницы в сове́т пра́ведных.
6 Я́ко весть Госпо́дь путь пра́ведных, и путь нечести́вых поги́бнет.
"""

md1_ChurchSlavonic_MorphAnalysisPromptBuilder = BusinessObjectFactory.create_md1_ChurchSlavonic_MorphAnalysisPromptBuilder()
res = md1_ChurchSlavonic_MorphAnalysisPromptBuilder.process(input_text)

print(res)