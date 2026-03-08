"""Add ages to hockey skaters and goalies master files.
Data source: Lineup Experts / Oct 2025 ranked list with ages as of Oct 2025.
"""
import csv, io, re, unicodedata

def normalize(name):
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = name.lower()
    name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name

# Known name mismatches: source name → canonical master name
NAME_MAP = {
    "johnjason peterka": "jj peterka",
    "matthew beniers": "matty beniers",
    "zachary bolduc": "zack bolduc",
    "matthew coronato": "matt coronato",
    "arseny gritsyuk": "arseniy gritsyuk",
    "jon marchessault": "jonathan marchessault",
    "matthew samoskevich": "mackie samoskevich",
    "joshua norris": "josh norris",
    "zachary benson": "zach benson",
    "matthew boldy": "matt boldy",
    "gabriel perreault": "gabe perreault",
    "matthew savoie": "matt savoie",
}

# Raw data: (rank, raw_name_with_team_pos, age)
RAW = """1\tMacklin Celebrini (SJ - C)\t19
2\tJack Hughes (NJ - C,LW)\t24
3\tConnor Bedard (CHI - C,RW)\t20
4\tCale Makar (COL - D)\t27
5\tMatthew Boldy (MIN - RW,LW)\t24
6\tConnor McDavid (EDM - C)\t29
7\tNathan MacKinnon (COL - C)\t30
8\tWyatt Johnston (DAL - C,RW)\t22
9\tAuston Matthews (TOR - C)\t28
10\tConnor Hellebuyck (WPG - G)\t32
11\tMatvei Michkov (PHI - RW,LW)\t21
12\tQuinn Hughes (MIN - D)\t26
13\tDavid Pastrnak (BOS - RW)\t29
14\tDylan Guenther (UTA - RW,LW)\t22
15\tJake Sanderson (OTT - D)\t23
16\tRasmus Dahlin (BUF - D)\t25
17\tLeon Draisaitl (EDM - C,LW)\t30
18\tTim Stutzle (OTT - C,LW)\t24
19\tEvan Bouchard (EDM - D)\t26
20\tKirill Kaprizov (MIN - LW)\t28
21\tNikita Kucherov (TB - RW)\t32
22\tBrady Tkachuk (OTT - LW,C)\t26
23\tJason Robertson (DAL - LW,RW)\t26
24\tSeth Jarvis (CAR - RW,LW,C)\t24
25\tJake Oettinger (DAL - G)\t27
26\tLane Hutson (MTL - D)\t22
27\tLucas Raymond (DET - RW)\t23
28\tThomas Harley (DAL - D)\t24
29\tCole Caufield (MTL - LW,RW)\t25
30\tLogan Cooley (UTA - C)\t21
31\tAndrei Vasilevskiy (TB - G)\t31
32\tAdam Fantilli (CBJ - C)\t21
33\tMatthew Knies (TOR - LW)\t23
34\tMoritz Seider (DET - D)\t24
35\tJack Eichel (VGS - C)\t29
36\tBrandon Hagel (TB - LW,RW)\t27
37\tMikko Rantanen (DAL - RW,LW)\t29
38\tKyle Connor (WPG - LW)\t29
39\tKirill Marchenko (CBJ - RW)\t25
40\tMatthew Schaefer (NYI - D)\t18
41\tFilip Gustavsson (MIN - G)\t27
42\tDustin Wolf (CGY - G)\t24
43\tWilliam Nylander (TOR - RW,C)\t29
44\tMartin Necas (COL - RW)\t27
45\tNick Suzuki (MTL - C)\t26
46\tSam Rinzel (CHI - D)\t21
47\tMitch Marner (VGS - RW,LW,C)\t28
48\tClayton Keller (UTA - LW,RW)\t27
49\tZach Werenski (CBJ - D)\t28
50\tZayne Parekh (CGY - D)\t20
51\tJuraj Slafkovsky (MTL - RW,LW)\t21
52\tCutter Gauthier (ANA - LW,RW)\t23
53\tJohn-Jason Peterka (UTA - LW,RW)\t24
54\tQuinton Byfield (LA - C,LW)\t23
55\tJesper Bratt (NJ - RW,LW)\t27
56\tIgor Shesterkin (NYR - G)\t30
57\tRobert Thomas (STL - C)\t26
58\tSam Reinhart (FLA - RW,C)\t30
59\tElias Pettersson (VAN - C,LW)\t27
60\tDylan Holloway (STL - LW,C)\t24
61\tMatthew Coronato (CGY - RW)\t23
62\tLeo Carlsson (ANA - C)\t21
63\tIvan Demidov (MTL - RW)\t20
64\tBrayden Point (TB - C)\t29
65\tMason McTavish (ANA - C)\t23
66\tPavel Dorofeyev (VGS - RW,LW)\t25
67\tNico Hischier (NJ - C)\t27
68\tBrock Faber (MIN - D)\t23
69\tMarco Rossi (VAN - C)\t24
70\tTrevor Zegras (PHI - LW,RW,C)\t24
71\tTage Thompson (BUF - C,RW)\t28
72\tLogan Stankoven (CAR - RW,C)\t23
73\tJake Guentzel (TB - LW,RW)\t31
74\tJordan Kyrou (STL - RW)\t27
75\tJiri Kulich (BUF - C)\t21
76\tFilip Forsberg (NSH - LW)\t31
77\tIlya Sorokin (NYI - G)\t30
78\tLukas Dostal (ANA - G)\t25
79\tJackson LaCombe (ANA - D)\t25
80\tNoah Dobson (MTL - D)\t26
81\tKent Johnson (CBJ - RW,LW,C)\t23
82\tAlex Laferriere (LA - RW,LW,C)\t24
83\tSebastian Aho (CAR - C)\t28
84\tAdrian Kempe (LA - RW)\t29
85\tMarco Kasper (DET - C,LW)\t21
86\tJakob Chychrun (WSH - D)\t27
87\tArtemi Panarin (LA - LW)\t34
88\tAndrei Svechnikov (CAR - LW,RW)\t25
89\tAdam Fox (NYR - D)\t28
90\tBrandt Clarke (LA - D)\t23
91\tDylan Cozens (OTT - C)\t25
92\tMiro Heiskanen (DAL - D)\t26
93\tAnton Lundell (FLA - C)\t24
94\tOwen Power (BUF - D)\t23
95\tCole Perfetti (WPG - RW,LW,C)\t24
96\tWill Smith (SJ - RW,C)\t20
97\tDrake Batherson (OTT - RW,LW)\t27
98\tAlex DeBrincat (DET - LW,RW)\t28
99\tMikhail Sergachev (UTA - D)\t27
100\tJuuse Saros (NSH - G)\t30
101\tAdin Hill (VGS - G)\t29
102\tConnor McMichael (WSH - LW,C)\t25
103\tJeremy Swayman (BOS - G)\t27
104\tFrank Nazar (CHI - C)\t22
105\tWilliam Eklund (SJ - LW,RW)\t23
106\tAlexander Nikishin (CAR - D)\t24
107\tSimon Edvinsson (DET - D)\t23
108\tDylan Larkin (DET - C)\t29
109\tMackenzie Blackwood (COL - G)\t29
110\tJ.T. Miller (NYR - C,RW,LW)\t32
111\tSergei Bobrovsky (FLA - G)\t37
112\tMark Scheifele (WPG - C)\t32
113\tMatthew Beniers (SEA - C)\t23
114\tJosh Morrissey (WPG - D)\t30
115\tShane Wright (SEA - C,RW)\t22
116\tDarcy Kuemper (LA - G)\t35
117\tLinus Ullmark (OTT - G)\t32
118\tTravis Konecny (PHI - RW,LW)\t28
119\tMichael Misa (SJ - C)\t19
120\tNikolaj Ehlers (CAR - LW,RW)\t30
121\tGabriel Vilardi (WPG - RW,C)\t26
122\tZachary Bolduc (MTL - RW,LW)\t23
123\tWill Cuylle (NYR - LW,RW)\t24
124\tBowen Byram (BUF - D)\t24
125\tMacKenzie Weegar (UTA - D)\t32
126\tMatthew Tkachuk (FLA - RW,LW)\t28
127\tJimmy Snuggerud (STL - RW)\t21
128\tLuke Hughes (NJ - D)\t22
129\tStuart Skinner (PIT - G)\t27
130\tOwen Tippett (PHI - LW,RW)\t27
131\tAlexis Lafreniere (NYR - RW,LW)\t24
132\tSpencer Knight (CHI - G)\t24
133\tAlex Tuch (BUF - RW,LW)\t29
134\tMorgan Geekie (BOS - LW,RW,C)\t27
135\tSam Montembeault (MTL - G)\t29
136\tJordan Binnington (STL - G)\t32
137\tAnthony Stolarz (TOR - G)\t32
138\tRoope Hintz (DAL - C)\t29
139\tYaroslav Askarov (SJ - G)\t23
140\tPhilip Broberg (STL - D)\t24
141\tKevin Fiala (LA - LW)\t29
142\tJackson Blake (CAR - RW)\t22
143\tVictor Hedman (TB - D)\t35
144\tUkko-Pekka Luukkonen (BUF - G)\t26
145\tRoman Josi (NSH - D)\t35
146\tJoel Eriksson Ek (MIN - C)\t29
147\tMathew Barzal (NYI - RW,C)\t28
148\tBo Horvat (NYI - C)\t30
149\tDylan Strome (WSH - C)\t29
150\tPierre-Luc Dubois (WSH - C,LW)\t27
151\tAliaksei Protas (WSH - LW,RW)\t25
152\tJoey Daccord (SEA - G)\t29
153\tConnor Zary (CGY - LW,RW,C)\t24
154\tTyson Foerster (PHI - LW,RW)\t24
155\tLogan Thompson (WSH - G)\t29
156\tSidney Crosby (PIT - C)\t38
157\tTimo Meier (NJ - LW,RW)\t29
158\tShane Pinto (OTT - C)\t25
159\tOlen Zellweger (ANA - D)\t22
160\tJared McCann (SEA - LW,C)\t29
161\tSean Durzi (UTA - D)\t27
162\tDougie Hamilton (NJ - D)\t32
163\tCarter Verhaeghe (FLA - LW)\t30
164\tJohn Tavares (TOR - C)\t35
165\tThatcher Demko (VAN - G)\t30
166\tDmitri Voronkov (CBJ - LW)\t25
167\tJacob Markstrom (NJ - G)\t36
168\tCharlie McAvoy (BOS - D)\t28
169\tKarel Vejmelka (UTA - G)\t29
170\tShea Theodore (VGS - D)\t30
171\tMika Zibanejad (NYR - C,RW)\t32
172\tJake Walman (EDM - D)\t30
173\tVince Dunn (SEA - D)\t29
174\tVincent Trocheck (NYR - C)\t32
175\tSam Bennett (FLA - C)\t29
176\tThomas Chabot (OTT - D)\t29
177\tAlexander Romanov (NYI - D)\t26
178\tBrandon Montour (SEA - D)\t31
179\tNazem Kadri (COL - C)\t35
180\tRickard Rakell (PIT - LW,RW,C)\t32
181\tNoah Hanifin (VGS - D)\t29
182\tRasmus Andersson (VGS - D)\t29
183\tAnthony Cirelli (TB - C)\t28
184\tPyotr Kochetkov (CAR - G)\t26
185\tBrock Boeser (VAN - RW,LW)\t29
186\tDevon Toews (COL - D)\t32
187\tJoseph Woll (TOR - G)\t27
188\tZach Hyman (EDM - RW,LW)\t33
189\tValeri Nichushkin (COL - RW,LW)\t31
190\tMaxim Shabanov (NYI - RW)\t25
191\tDarnell Nurse (EDM - D)\t31
192\tPavel Buchnevich (STL - RW,LW,C)\t30
193\tSean Monahan (CBJ - C)\t31
194\tTroy Terry (ANA - RW)\t28
195\tBarrett Hayton (UTA - C)\t25
196\tMorgan Rielly (TOR - D)\t31
197\tBryan Rust (PIT - RW)\t33
198\tGustav Forsling (FLA - D)\t29
199\tAlex Vlasic (CHI - D)\t24
200\tTom Wilson (WSH - RW)\t31
201\tArtturi Lehkonen (COL - LW,RW)\t30
202\tNeal Pionk (WPG - D)\t30
203\tTomas Hertl (VGS - C,LW)\t32
204\tFrank Vatrano (ANA - LW,C)\t31
205\tConor Garland (CBJ - RW)\t29
206\tAaron Ekblad (FLA - D)\t30
207\tFrederik Andersen (CAR - G)\t36
208\tJohn Carlson (ANA - D)\t36
209\tErik Karlsson (PIT - D)\t35
210\tRyan Nugent-Hopkins (EDM - LW,C)\t32
211\tDylan Samberg (WPG - D)\t27
212\tNick Schmaltz (UTA - RW,C)\t30
213\tCole Sillinger (CBJ - C,RW)\t22
214\tDawson Mercer (NJ - RW,C)\t24
215\tMark Stone (VGS - RW)\t33
216\tColton Parayko (STL - D)\t32
217\tK'Andre Miller (CAR - D)\t26
218\tTyler Toffoli (SJ - RW,LW)\t33
219\tMatthew Samoskevich (FLA - RW)\t23
220\tKaapo Kakko (SEA - RW)\t25
221\tDante Fabbro (CBJ - D)\t27
222\tArseny Gritsyuk (NJ - RW,LW)\t24
223\tJake Neighbours (STL - LW,RW)\t23
224\tFilip Hronek (VAN - D)\t28
225\tSimon Holmstrom (NYI - RW)\t24
226\tJake Debrusk (VAN - LW,RW)\t29
227\tFilip Chytil (VAN - C)\t26
228\tGabriel Landeskog (COL - LW,RW)\t33
229\tKaiden Guhle (MTL - D)\t24
230\tSeth Jones (FLA - D)\t31
231\tRidly Greig (OTT - C,RW,LW)\t23
232\tDenton Mateychuk (CBJ - D)\t21
233\tShayne Gostisbehere (CAR - D)\t32
234\tMichael Kesselring (BUF - D)\t26
235\tAlex Ovechkin (WSH - LW,RW)\t40
236\tZachary Benson (BUF - LW)\t20
237\tJohn Gibson (DET - G)\t32
238\tJoshua Norris (BUF - C)\t26
239\tBrock Nelson (COL - C)\t34
240\tMason Marchment (CBJ - LW)\t30
241\tBraden Schneider (NYR - D)\t24
242\tJaccob Slavin (CAR - D)\t31
243\tJosh Doan (BUF - RW,LW)\t24
244\tSteven Stamkos (NSH - C,RW,LW)\t36
245\tAnthony DeAngelo (NYI - D)\t30
246\tRyan Leonard (WSH - RW)\t21
247\tJack Quinn (BUF - RW)\t24
248\tFabian Zetterlund (OTT - RW,LW)\t26
249\tDrew Doughty (LA - D)\t36
250\tElias Lindholm (BOS - C)\t31
251\tJon Marchessault (NSH - RW)\t35
252\tMattias Ekholm (EDM - D)\t35
253\tEsa Lindell (DAL - D)\t31
254\tRyan Donato (CHI - LW,RW,C)\t29
255\tSamuel Ersson (PHI - G)\t26
256\tAnders Lee (NYI - LW)\t35
257\tMatt Duchene (DAL - C,RW)\t35
258\tTravis Sanheim (PHI - D)\t29
259\tIvan Barbashev (VGS - LW)\t30
260\tBoone Jenner (CBJ - C,LW)\t32
261\tWarren Foegele (OTT - LW,RW)\t29
262\tChris Kreider (ANA - LW)\t34
263\tMikey Anderson (LA - D)\t26
264\tTyler Seguin (DAL - RW,C)\t34
265\tMorgan Frost (CGY - C)\t26
266\tElvis Merzlikins (CBJ - G)\t31
267\tPavel Zacha (BOS - C,LW)\t28
268\tCameron York (PHI - D)\t25
269\tJonathan Huberdeau (CGY - LW,C)\t32
270\tJordan Spence (OTT - D)\t25
271\tJamie Drysdale (PHI - D)\t23
272\tZeev Buium (VAN - D)\t20
273\tBrady Skjei (NSH - D)\t31
274\tDarren Raddysh (TB - D)\t30
275\tBlake Coleman (CGY - RW,LW,C)\t34
276\tRasmus Sandin (WSH - D)\t26
277\tRyan O'Reilly (NSH - C)\t35
278\tPatrik Laine (MTL - RW,LW)\t27
279\tVladislav Gavrikov (NYR - D)\t30
280\tJustin Faulk (DET - D)\t33
281\tTrevor Moore (LA - RW,LW)\t30
282\tSamuel Girard (PIT - D)\t27
283\tJet Greaves (CBJ - G)\t24
284\tLuke Evangelista (NSH - RW)\t24
285\tJesperi Kotkaniemi (CAR - C)\t25
286\tBrad Marchand (FLA - LW,RW)\t37
287\tBobby McMann (SEA - LW)\t29
288\tWilliam Karlsson (VGS - C)\t33
289\tIvan Provorov (CBJ - D)\t29
290\tHampus Lindholm (BOS - D)\t32
291\tMatias Maccelli (TOR - LW,RW)\t25
292\tJacob Middleton (MIN - D)\t30
293\tMike Matheson (MTL - D)\t32
294\tAnze Kopitar (LA - C)\t38
295\tPatrick Kane (DET - RW)\t37
296\tRyan Pulock (NYI - D)\t31
297\tPhillip Danault (MTL - C)\t33
298\tCasey Mittelstadt (BOS - C,LW)\t27
299\tMatt Roy (WSH - D)\t31
300\tMikael Granlund (ANA - C,RW,LW)\t34
301\tBrayden McNabb (VGS - D)\t35
302\tMarcus Pettersson (VAN - D)\t29
303\tJonas Brodin (MIN - D)\t32
304\tAdam Larsson (SEA - D)\t33
305\tJacob Trouba (ANA - D)\t32
306\tJake McCabe (TOR - D)\t32
307\tKris Letang (PIT - D)\t38
308\tMason Lohrei (BOS - D)\t25
309\tJaden Schwartz (SEA - LW,C)\t33
310\tMats Zuccarello (MIN - RW)\t38
311\tRyan McLeod (BUF - C)\t26
312\tSam Malinski (COL - D)\t27
313\tJared Spurgeon (MIN - D)\t36
314\tNick Seeler (PHI - D)\t32
315\tNikita Zadorov (BOS - D)\t30
316\tDylan DeMelo (WPG - D)\t32
317\tEvgeni Malkin (PIT - C,RW,LW)\t39
318\tMartin Fehervary (WSH - D)\t26
319\tRoss Colton (COL - LW,C)\t29
320\tPius Suter (STL - C,LW)\t29
321\tEeli Tolvanen (SEA - LW,RW)\t26
322\tViktor Arvidsson (BOS - RW,LW)\t32
323\tCam Fowler (STL - D)\t34
324\tMatt Grzelcyk (CHI - D)\t32
325\tBrent Burns (COL - D)\t40
326\tOliver Ekman-Larsson (TOR - D)\t34
327\tNiko Mikkola (FLA - D)\t29
328\tEvan Rodrigues (FLA - LW,RW,C)\t32
329\tYegor Sharangovich (CGY - LW,RW,C)\t27
330\tTeuvo Teravainen (CHI - LW,RW)\t31
331\tScott Morrow (NYR - D)\t23
332\tBrett Pesce (NJ - D)\t31
333\tBrayden Schenn (NYI - C,LW)\t34
334\tKyle Palmieri (NYI - RW)\t35
335\tDamon Severson (CBJ - D)\t31
336\tSean Couturier (PHI - C)\t33
337\tJason Zucker (BUF - LW)\t34
338\tMikael Backlund (CGY - C)\t36
339\tRyan McDonagh (TB - D)\t36
340\tNoah Cates (PHI - C)\t27
341\tJamie Benn (DAL - LW,RW,C)\t36
342\tTyler Myers (DAL - D)\t36
343\tEvander Kane (VAN - LW)\t34
344\tStefan Noesen (NJ - RW,LW)\t33
345\tVladimir Tarasenko (MIN - RW,LW)\t34
346\tRadko Gudas (ANA - D)\t35
347\tDmitry Orlov (SJ - D)\t34
348\tSean Walker (CAR - D)\t31
349\tRasmus Ristolainen (PHI - D)\t31
350\tChris Tanev (TOR - D)\t36
351\tBrett Kulak (COL - D)\t32
352\tTimothy Liljegren (WSH - D)\t26
353\tCody Ceci (LA - D)\t32
354\tJalen Chatfield (CAR - D)\t29
355\tTyler Bertuzzi (CHI - RW,LW)\t31
356\tBrandon Carlo (TOR - D)\t29
357\tBrett Howden (VGS - LW,C)\t27
358\tArtem Zub (OTT - D)\t30
359\tAlexandre Carrier (MTL - D)\t29
360\tJeff Skinner (N/A - LW)\t33
361\tOlli Maatta (CGY - D)\t31
362\tChandler Stephenson (SEA - C)\t31
363\tJ.J. Moser (TB - D)\t25
364\tIan Cole (UTA - D)\t37
365\tClaude Giroux (OTT - RW,LW)\t38
366\tNino Niederreiter (WPG - LW,RW)\t33
367\tMax Domi (TOR - C,LW)\t31
368\tRyan Lindgren (SEA - D)\t28
369\tAlex Iafallo (WPG - RW,LW,C)\t32
370\tTrent Frederic (EDM - LW,RW,C)\t28
371\tRyan Hartman (MIN - C,RW)\t31
372\tAnthony Mantha (PIT - RW,LW)\t31
373\tKevin Bahl (CGY - D)\t25
374\tAdam Pelech (NYI - D)\t31
375\tAlec Martinez (N/A - D)\t38
376\tErik Cernak (TB - D)\t28
377\tConnor Murphy (EDM - D)\t32
378\tAndrei Kuzmenko (LA - LW,RW)\t30
379\tOliver Bjorkstrand (TB - RW)\t30
380\tBlake Wheeler (N/A - RW)\t39
381\tTrevor van Riemsdyk (WSH - D)\t34
382\tVladislav Namestnikov (WPG - C,LW)\t33
383\tYegor Chinakhov (PIT - LW,RW)\t25
384\tJack Roslovic (EDM - RW,C)\t29
385\tLogan Mailloux (STL - D)\t22
386\tJean-Gabriel Pageau (NYI - C,RW)\t33
387\tReilly Smith (VGS - RW)\t34
388\tMaxim Tsyplakov (NJ - LW,RW)\t27
389\tConor Geekie (TB - C)\t21
390\tSimon Nemec (NJ - D)\t22
391\tMario Ferraro (SJ - D)\t27
392\tJonathan Toews (WPG - C)\t37
393\tBobby Brink (MIN - RW)\t24
394\tTristan Jarry (EDM - G)\t30
395\tNick Bjugstad (NJ - C)\t33
396\tConor Timmins (BUF - D)\t27
397\tPavel Mintyukov (ANA - D)\t22
398\tDanila Yurov (MIN - RW,C)\t22
399\tVictor Soderstrom (BOS - D)\t25
400\tMartin Pospisil (CGY - RW,C)\t26
401\tMatthew Poitras (BOS - C)\t21
402\tNicholas Robertson (TOR - RW)\t24
403\tRyker Evans (SEA - D)\t24
404\tKirby Dach (MTL - C,RW)\t25
405\tPhillip Tomasino (PHI - RW,C)\t24
406\tAndrew Peeke (BOS - D)\t27
407\tNick Paul (TB - C,LW)\t30
408\tVille Koivunen (PIT - RW)\t22
409\tNicolas Roy (COL - C,RW)\t29
410\tJoel Farabee (CGY - LW,RW)\t26
411\tAlexander Wennberg (SJ - C)\t31
412\tJ.T. Compher (DET - C)\t30
413\tJonathan Drouin (STL - LW,RW)\t30
414\tMavrik Bourque (DAL - RW,C)\t24
415\tBen Chiarot (DET - D)\t34
416\tIsaac Howard (EDM - LW)\t21
417\tJustin Barron (NSH - D)\t24
418\tMichael Bunting (DAL - LW)\t30
419\tNick Perbix (NSH - D)\t27
420\tDrew Helleson (ANA - D)\t24
421\tWilliam Borgen (NYR - D)\t29
422\tFedor Svechkov (NSH - C)\t22
423\tWyatt Kaiser (CHI - D)\t23
424\tVasily Podkolzin (EDM - LW,RW)\t24
425\tFraser Minten (BOS - C)\t21
426\tNick Blankenburg (COL - D)\t27
427\tKiefer Sherwood (SJ - RW,LW)\t30
428\tEetu Luostarinen (FLA - LW)\t27
429\tArtyom Levshunov (CHI - D)\t20
430\tJani Hakanpaa (N/A - D)\t33
431\tAlex Killorn (ANA - RW,LW,C)\t36
432\tRutger McGroarty (PIT - RW)\t21
433\tLian Bichsel (DAL - D)\t21
434\tGabriel Perreault (NYR - RW)\t20
435\tCameron Lund (SJ - C)\t21
436\tCharlie Lindgren (WSH - G)\t32
437\tMichael Rasmussen (DET - LW,C)\t26
438\tConnor Clifton (PIT - D)\t30
439\tElmer Soderblom (PIT - LW)\t24
440\tJoel Blomqvist (PIT - G)\t24
441\tLiam Ohgren (VAN - LW)\t22
442\tSam Colangelo (ANA - RW)\t24
443\tLeevi Merilainen (OTT - G)\t23
444\tAlex Turcotte (LA - LW,C)\t25
445\tNils Lundkvist (DAL - D)\t25
446\tMattias Samuelsson (BUF - D)\t25
447\tDevon Levi (BUF - G)\t24
448\tBradly Nadeau (CAR - LW)\t20
449\tJack Drury (COL - C)\t26
450\tTristan Luneau (ANA - D)\t22
451\tJoel Hofer (STL - G)\t25
452\tCalen Addison (NJ - D)\t25
453\tAatu Raty (VAN - C)\t23
454\tCam Talbot (DET - G)\t38
455\tJordan Martinook (CAR - LW)\t33
456\tIlya Samsonov (N/A - G)\t29
457\tJack McBain (UTA - LW,C)\t26
458\tAlex Bump (PHI - LW)\t22
459\tTommy Novak (PIT - C,LW)\t28
460\tRyan Strome (CGY - C)\t32
461\tFilip Hallander (PIT - C)\t25
462\tZach Whitecloud (CGY - D)\t29
463\tJesper Wallstedt (MIN - G)\t23
464\tZachary L'Heureux (NSH - LW)\t22
465\tNils Hoglander (VAN - LW)\t25
466\tHendrix Lapierre (WSH - C)\t24
467\tAdam Wilsby (NSH - D)\t25
468\tKevin Lankinen (VAN - G)\t30
469\tMatthew Savoie (EDM - C,RW)\t22
470\tAlex Newhook (MTL - LW,C)\t25
471\tZachary Jones (BUF - D)\t25
472\tJonathan Lekkerimaki (VAN - RW)\t21
473\tAkira Schmid (VGS - G)\t25
474\tNicolas Hague (NSH - D)\t27
475\tOliver Moore (CHI - C)\t21
476\tArturs Silovs (PIT - G)\t24
477\tKaedan Korczak (VGS - D)\t25
478\tLuca Del Bel Belluz (CBJ - C)\t22
479\tJakub Dobes (MTL - G)\t24
480\tJordan Eberle (SEA - RW)\t35
481\tEmil Heineman (NYI - LW,RW)\t24
482\tJani Nyman (SEA - RW)\t21
483\tOliver Kapanen (MTL - C)\t22
484\tMatthew Wood (NSH - RW)\t21
485\tLuca Cagnoni (SJ - D)\t21
486\tRyan Poehling (ANA - C)\t27
487\tArthur Kaliyev (OTT - RW)\t24
488\tOwen Beck (MTL - C)\t22
489\tConnor Ingram (EDM - G)\t28
490\tJohn Marino (UTA - D)\t28
491\tAdam Lowry (WPG - C)\t32
492\tArvid Soderblom (CHI - G)\t26
493\tThomas Bordeleau (STL - C)\t24
494\tJonatan Berggren (STL - RW)\t25
495\tLukas Reichel (BOS - LW)\t23
496\tPeyton Krebs (BUF - C)\t25
497\tCollin Graf (SJ - RW,LW)\t23
498\tHenri Jokiharju (BOS - D)\t26
499\tLawson Crouse (UTA - RW,LW)\t28
500\tIvan Miroshnichenko (WSH - LW)\t22"""

# Parse raw data
def parse_raw(raw):
    skater_ages = {}
    goalie_ages = {}
    for line in raw.strip().splitlines():
        parts = line.split('\t')
        if len(parts) < 3:
            continue
        name_team = parts[1].strip()
        age = int(parts[2].strip())
        # Extract name: everything before the '('
        name = name_team[:name_team.index('(')].strip()
        # Extract positions: between '-' and ')'
        inner = name_team[name_team.index('(')+1:name_team.index(')')]
        pos_part = inner.split('-')[1].strip()
        positions = [p.strip() for p in pos_part.split(',')]
        is_goalie = positions == ['G']
        key = normalize(name)
        key = NAME_MAP.get(key, key)
        if is_goalie:
            goalie_ages[key] = age
        else:
            skater_ages[key] = age
    return skater_ages, goalie_ages

skater_ages, goalie_ages = parse_raw(RAW)

def update_master(path, age_lookup):
    with open(path, newline='', encoding='utf-8') as f:
        rows = list(csv.reader(f))
    header = rows[0]
    age_idx = header.index('Age')
    matched = 0
    unmatched = []
    for row in rows[1:]:
        if not row:
            continue
        key = normalize(row[0])
        if key in age_lookup:
            row[age_idx] = age_lookup[key]
            matched += 1
        else:
            unmatched.append(row[0])
    out = io.StringIO()
    csv.writer(out).writerows(rows)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        f.write(out.getvalue())
    return matched, unmatched

sk_matched, sk_unmatched = update_master('hockey/hockey_skaters_master.csv', skater_ages)
go_matched, go_unmatched = update_master('hockey/hockey_goalies_master.csv', goalie_ages)

print(f"Skaters: {sk_matched} matched, {len(sk_unmatched)} unmatched")
print(f"Goalies: {go_matched} matched, {len(go_unmatched)} unmatched")
print("\nUnmatched skaters:")
for p in sk_unmatched:
    print(f"  {p}")
print("\nUnmatched goalies:")
for p in go_unmatched:
    print(f"  {p}")
