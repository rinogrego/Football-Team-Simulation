fbref = [
    # index
    'Player',
    # post-match player information/stats
    "Pos",
    "Age",
    "Min",
    # pre-match player information/stats
    'standard - Nation',
    'standard - Pos',
    'standard - Age',
    'standard - MP',
    'standard - Playing Time - Starts',
    'standard - Playing Time - Min',
    'standard - Playing Time - 90s',
    'standard - Performance - Gls',
    'standard - Performance - Ast',
    'standard - Performance - G-PK',
    'standard - Performance - PK',
    'standard - Performance - PKatt',
    'standard - Performance - CrdY',
    'standard - Performance - CrdR',
    'standard - Per 90 Minutes - Gls',
    'standard - Per 90 Minutes - Ast',
    'standard - Per 90 Minutes - G+A',
    'standard - Per 90 Minutes - G-PK',
    'standard - Per 90 Minutes - G+A-PK',
    'standard - Expected - xG',
    'standard - Expected - npxG',
    'standard - Expected - xAG',
    'standard - Expected - npxG+xAG',
    'standard - Per 90 Minutes - xG',
    'standard - Per 90 Minutes - xAG',
    'standard - Per 90 Minutes - xG+xAG',
    'standard - Per 90 Minutes - npxG',
    'standard - Per 90 Minutes - npxG+xAG',
    'keeper - Nation',
    'keeper - Pos',
    'keeper - Age',
    'keeper - Playing Time - MP',
    'keeper - Playing Time - Starts',
    'keeper - Playing Time - Min',
    'keeper - Playing Time - 90s',
    'keeper - Performance - GA',
    'keeper - Performance - GA90',
    'keeper - Performance - SoTA',
    'keeper - Performance - Saves',
    'keeper - Performance - Save%',
    'keeper - Performance - W',
    'keeper - Performance - D',
    'keeper - Performance - L',
    'keeper - Performance - CS',
    'keeper - Performance - CS%',
    'keeper - Penalty Kicks - PKatt',
    'keeper - Penalty Kicks - PKA',
    'keeper - Penalty Kicks - PKsv',
    'keeper - Penalty Kicks - PKm',
    'keeper - Penalty Kicks - Save%',
    'keeper_adv - Nation',
    'keeper_adv - Pos',
    'keeper_adv - Age',
    'keeper_adv - 90s',
    'keeper_adv - Goals - GA',
    'keeper_adv - Goals - PKA',
    'keeper_adv - Goals - FK',
    'keeper_adv - Goals - CK',
    'keeper_adv - Goals - OG',
    'keeper_adv - Expected - PSxG',
    'keeper_adv - Expected - PSxG/SoT',
    'keeper_adv - Expected - PSxG+/-',
    'keeper_adv - Expected - /90',
    'keeper_adv - Launched - Cmp',
    'keeper_adv - Launched - Att',
    'keeper_adv - Launched - Cmp%',
    'keeper_adv - Passes - Att',
    'keeper_adv - Passes - Thr',
    'keeper_adv - Passes - Launch%',
    'keeper_adv - Passes - AvgLen',
    'keeper_adv - Goal Kicks - Att',
    'keeper_adv - Goal Kicks - Launch%',
    'keeper_adv - Goal Kicks - AvgLen',
    'keeper_adv - Crosses - Opp',
    'keeper_adv - Crosses - Stp',
    'keeper_adv - Crosses - Stp%',
    'keeper_adv - Sweeper - #OPA',
    'keeper_adv - Sweeper - #OPA/90',
    'keeper_adv - Sweeper - AvgDist',
    'shooting - Nation',
    'shooting - Pos',
    'shooting - Age',
    'shooting - 90s',
    'shooting - Standard - Gls',
    'shooting - Standard - Sh',
    'shooting - Standard - SoT',
    'shooting - Standard - SoT%',
    'shooting - Standard - Sh/90',
    'shooting - Standard - SoT/90',
    'shooting - Standard - G/Sh',
    'shooting - Standard - G/SoT',
    'shooting - Standard - Dist',
    'shooting - Standard - FK',
    'shooting - Standard - PK',
    'shooting - Standard - PKatt',
    'shooting - Expected - xG',
    'shooting - Expected - npxG',
    'shooting - Expected - npxG/Sh',
    'shooting - Expected - G-xG',
    'shooting - Expected - np:G-xG',
    'passing - Nation',
    'passing - Pos',
    'passing - Age',
    'passing - 90s',
    'passing - Ast',
    'passing - xAG',
    'passing - xA',
    'passing - A-xAG',
    'passing - KP',
    'passing - 1/3',
    'passing - PPA',
    'passing - CrsPA',
    'passing - Prog',
    'passing - Total - Cmp',
    'passing - Total - Att',
    'passing - Total - Cmp%',
    'passing - Total - TotDist',
    'passing - Total - PrgDist',
    'passing - Short - Cmp',
    'passing - Short - Att',
    'passing - Short - Cmp%',
    'passing - Medium - Cmp',
    'passing - Medium - Att',
    'passing - Medium - Cmp%',
    'passing - Long - Cmp',
    'passing - Long - Att',
    'passing - Long - Cmp%',
    'passing_types - Nation',
    'passing_types - Pos',
    'passing_types - Age',
    'passing_types - 90s',
    'passing_types - Att',
    'passing_types - Pass Types - Live',
    'passing_types - Pass Types - Dead',
    'passing_types - Pass Types - FK',
    'passing_types - Pass Types - TB',
    'passing_types - Pass Types - Sw',
    'passing_types - Pass Types - Crs',
    'passing_types - Pass Types - TI',
    'passing_types - Pass Types - CK',
    'passing_types - Corner Kicks - In',
    'passing_types - Corner Kicks - Out',
    'passing_types - Corner Kicks - Str',
    'passing_types - Outcomes - Cmp',
    'passing_types - Outcomes - Off',
    'passing_types - Outcomes - Blocks',
    'gca - Nation',
    'gca - Pos',
    'gca - Age',
    'gca - 90s',
    'gca - SCA - SCA',
    'gca - SCA - SCA90',
    'gca - SCA Types - PassLive',
    'gca - SCA Types - PassDead',
    'gca - SCA Types - Drib',
    'gca - SCA Types - Sh',
    'gca - SCA Types - Fld',
    'gca - SCA Types - Def',
    'gca - GCA - GCA',
    'gca - GCA - GCA90',
    'gca - GCA Types - PassLive',
    'gca - GCA Types - PassDead',
    'gca - GCA Types - Drib',
    'gca - GCA Types - Sh',
    'gca - GCA Types - Fld',
    'gca - GCA Types - Def',
    'defense - Nation',
    'defense - Pos',
    'defense - Age',
    'defense - 90s',
    'defense - Int',
    'defense - Tkl+Int',
    'defense - Clr',
    'defense - Err',
    'defense - Tackles - Tkl',
    'defense - Tackles - TklW',
    'defense - Tackles - Def 3rd',
    'defense - Tackles - Mid 3rd',
    'defense - Tackles - Att 3rd',
    'defense - Vs Dribbles - Tkl',
    'defense - Vs Dribbles - Att',
    'defense - Vs Dribbles - Tkl%',
    'defense - Vs Dribbles - Past',
    'defense - Blocks - Blocks',
    'defense - Blocks - Sh',
    'defense - Blocks - Pass',
    'possession - Nation',
    'possession - Pos',
    'possession - Age',
    'possession - 90s',
    'possession - Touches - Touches',
    'possession - Touches - Def Pen',
    'possession - Touches - Def 3rd',
    'possession - Touches - Mid 3rd',
    'possession - Touches - Att 3rd',
    'possession - Touches - Att Pen',
    'possession - Touches - Live',
    'possession - Dribbles - Succ',
    'possession - Dribbles - Att',
    'possession - Dribbles - Succ%',
    'possession - Dribbles - Mis',
    'possession - Dribbles - Dis',
    'possession - Receiving - Rec',
    'possession - Receiving - Prog',
    'playing_time - Nation',
    'playing_time - Pos',
    'playing_time - Age',
    'playing_time - MP',
    'playing_time - Playing Time - Min',
    'playing_time - Playing Time - Mn/MP',
    'playing_time - Playing Time - Min%',
    'playing_time - Playing Time - 90s',
    'playing_time - Starts - Starts',
    'playing_time - Starts - Mn/Start',
    'playing_time - Starts - Compl',
    'playing_time - Subs - Subs',
    'playing_time - Subs - Mn/Sub',
    'playing_time - Subs - unSub',
    'playing_time - Team Success - PPM',
    'playing_time - Team Success - onG',
    'playing_time - Team Success - onGA',
    'playing_time - Team Success - +/-',
    'playing_time - Team Success - +/-90',
    'playing_time - Team Success - On-Off',
    'playing_time - Team Success (xG) - onxG',
    'playing_time - Team Success (xG) - onxGA',
    'playing_time - Team Success (xG) - xG+/-',
    'playing_time - Team Success (xG) - xG+/-90',
    'playing_time - Team Success (xG) - On-Off',
    'misc - Nation',
    'misc - Pos',
    'misc - Age',
    'misc - 90s',
    'misc - Performance - CrdY',
    'misc - Performance - CrdR',
    'misc - Performance - 2CrdY',
    'misc - Performance - Fls',
    'misc - Performance - Fld',
    'misc - Performance - Off',
    'misc - Performance - Crs',
    'misc - Performance - Int',
    'misc - Performance - TklW',
    'misc - Performance - PKwon',
    'misc - Performance - PKcon',
    'misc - Performance - OG',
    'misc - Performance - Recov',
    'misc - Aerial Duels - Won',
    'misc - Aerial Duels - Lost',
    'misc - Aerial Duels - Won%',
]