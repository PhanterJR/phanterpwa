# -*- coding: utf-8 -*-
import random
from .helpers import DIV, XML

attributes = {
    'red': 'cor vermelha',
    'yellow': 'cor amarela',
    'pink': 'cor rosa',
    'black': 'cor preta',
    'white': 'cor branco',
    'blue': 'cor azul',
    'green': 'cor verde',
    'grey': 'cor cinza',
    'square': 'formato de quadrado',
    'circle': 'formato de círculo',
    'star': 'formato de estrela',
    'triangle': 'formato de triângulo',
    'number': 'um número',
    'number one': 'o número um',
    'number two': 'o número dois',
    'number three': 'o número três',
    'number four': 'o número quatro',
    'letter': 'uma letra',
    'letter a': 'a letra a',
    'letter b': 'a letra b',
    'letter c': 'a letra c',
    'letter d': 'a letra d',
    'arrow': 'uma seta',
    'arrow up': 'uma seta para cima',
    'arrow down': 'uma seta para baixo',
    'arrow left': 'uma seta para esquerda',
    'arrow right': 'uma seta para direita',
    'mean of transport': 'um meio de transporte',
    'airplane': 'um avião',
    'car': 'um carro',
    'motorcycle': 'uma motocicleta',
    'ship': 'um barco'
}
svg_forms = {
    11: '<svg class="captcha-option-11" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><rect class="fil0" x="1.99918" y="1.99918" width="46.0018" height="46.0018"/><path class="fil1" d="M29.9667 35.5263c0,0.229141 -0.105121,0.440565 -0.31064,0.633091 -0.204337,0.191345 -0.427573,0.291741 -0.669706,0.291741 -0.583483,0 -1.45753,0.0059057 -2.61741,0.0177171 -1.16697,0.0129925 -2.03628,0.0188982 -2.61859,0.0188982 -0.446471,0 -0.670887,-0.192526 -0.657895,-0.583483l0.0188982 -0.198431c0.173628,-4.62889 0.253945,-7.43291 0.253945,-8.41916l0 -5.39781c0,-0.335444 -0.0874043,-0.57049 -0.236228,-0.509071 -1.74336,0.716952 -3.77847,2.43079 -5.74388,2.43079 -0.379146,0 -0.564585,-0.229141 -0.564585,-0.676793 0,-0.409855 -0.00708684,-1.02995 -0.0188982,-1.85439 -0.0118114,-0.81853 -0.0188982,-1.44571 -0.0188982,-1.86856 0,-0.240952 0.138193,-0.491354 0.453558,-0.545686 1.9855,-0.338987 6.87778,-3.39814 7.72938,-4.97378 0.15591,-0.287017 0.385051,-0.379146 0.527969,-0.379146 0.0248039,0 0.0992157,0.0129925 0.21733,0.0377965 0.465369,0.09331 1.14807,0.248039 2.05282,0.452376 0.484267,0.0626004 1.19768,0.167722 2.12841,0.329538 0.167722,0.042521 0.253945,0.179533 0.253945,0.396863 0,0.0744118 -0.0118114,0.198431 -0.0366153,0.385051 -0.129925,1.06066 -0.198431,3.67216 -0.198431,7.82977 0,1.39611 0.0059057,3.49263 0.0248039,6.29075 0.0188982,2.79812 0.0307096,4.89582 0.0307096,6.29193z"/></svg>',
    12: '<svg class="captcha-option-12" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><rect class="fil0" x="1.99898" y="1.99898" width="46.0018" height="46.0018"/><path class="fil1" d="M24.8972 20.5436c-0.220873,0.464188 -0.600019,1.46934 -1.12326,3.02017 -0.572853,1.64769 -0.85987,2.61386 -0.85987,2.90088 0,0.188982 0.318908,0.291741 0.950817,0.313002 0.329538,0.0212605 0.864594,0.0318908 1.6158,0.0318908 0.696872,0 1.08074,-0.0862232 1.15634,-0.252764 0.0212605,-0.0543324 0.0318908,-0.125201 0.0318908,-0.222054 0,-0.346074 -0.243315,-1.30752 -0.728763,-2.87962 -0.475999,-1.51776 -0.820892,-2.48984 -1.04295,-2.91151zm11.2196 14.4182c0,0.188982 -0.13465,0.318908 -0.393319,0.394501 -0.318908,0.0862232 -1.3028,0.12402 -2.94458,0.12402 -1.51304,0 -2.47921,-0.0377965 -2.91151,-0.12402 -0.36261,-0.0755929 -0.589389,-0.313002 -0.681518,-0.713408 -0.361429,-1.51776 -0.64254,-2.32803 -0.842153,-2.43551 -0.167722,-0.0767741 -1.58273,-0.114571 -4.24029,-0.114571 -1.79415,0 -2.74969,0.0496079 -2.86308,0.146461 -0.178352,0.167722 -0.377965,0.734669 -0.600019,1.69021 -0.205518,0.875224 -0.442927,1.35122 -0.728763,1.42682 -0.36261,0.0862232 -1.56147,0.12402 -3.60838,0.12402 -1.6158,0 -2.42134,-0.151186 -2.42134,-0.459463 0,-0.2693 1.18941,-3.64027 3.57649,-10.1129 2.58197,-6.99471 3.98753,-10.8358 4.2084,-11.5326 0.12402,-0.405131 0.275206,-0.604743 0.442927,-0.604743 0.287017,0 0.724039,0.0271662 1.32406,0.0803175 0.594113,0.0543324 1.04177,0.0814986 1.33351,0.0814986 0.287017,0 0.707503,-0.0212605 1.25909,-0.059057 0.556317,-0.0330719 0.967353,-0.0543324 1.24256,-0.0543324 0.199613,0 0.38387,0.172446 0.556317,0.524426 0.512615,1.10673 2.02565,4.90409 4.52731,11.3921 2.50638,6.5317 3.76429,9.93929 3.76429,10.2263z"/></svg>',
    13: '<svg class="captcha-option-13" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><rect class="fil0" x="1.99918" y="1.99898" width="46.0018" height="46.0018"/><path class="fil1" d="M28.8399 35.8499l0 -11.8551 3.43948 0 -7.27936 -9.8448 -7.27818 9.8448 3.4383 0 0 11.8551 7.67977 0zm0 -5.92814m1.71974 -5.92696m-1.92053 -4.92299m-7.27818 0m-1.92053 4.92299m1.71974 5.92696m3.83988 5.92814"/></svg>',
    14: '<svg class="captcha-option-14" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><rect class="fil0" x="1.99898" y="1.99918" width="46.0018" height="46.0018"/><path class="fil1" d="M9.2625 35.2629l1.0524 2.36937 24.3516 0.131106c3.34026,-1.47997 5.17221,-3.56468 6.3191,-5.92341l-31.723 3.42294zm2.48394 -1.11972l10.7625 -1.33233 14.2634 -1.7599c-1.71265,-9.79047 -12.6098,-17.9049 -14.3319,-19.1262l-0.016536 -2.05164c-2.01266,2.18275 -3.33436,1.76698 -5.44505,4.18005 2.42842,-1.02523 2.91623,-0.405131 5.11433,-1.102 -0.0106303,1.04885 -0.0212605,2.0977 -0.0318908,3.14656 -2.59969,6.56359 -5.96121,12.7102 -10.3149,18.0455zm10.8594 -1.6784l-0.157092 -19.4345c1.02641,5.47813 2.20283,11.9815 0.157092,19.4345z"/></svg>',
    21: '<svg class="captcha-option-21" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><circle class="fil0" cx="25" cy="24.9998" r="23.0008"/><path class="fil1" d="M33.979 30.6305c0,0.278749 -0.0318908,0.69451 -0.09331,1.25319 -0.0626004,0.558679 -0.09331,0.980346 -0.09331,1.27209 0,0.291741 -0.0059057,0.751205 -0.0118114,1.3713 -0.0129925,0.626004 -0.0188982,1.09137 -0.0188982,1.39611 0,0.297647 -0.205518,0.452376 -0.602381,0.452376 -0.148824,0 -0.713408,-0.118114 -1.70557,-0.347255 -1.10437,-0.242134 -3.16427,-0.360248 -6.18681,-0.360248 -0.930738,0 -2.33275,0.0496079 -4.19423,0.150005 -1.86738,0.105121 -3.2564,0.154729 -4.16234,0.154729 -0.316545,0 -0.490173,-0.148824 -0.527969,-0.453558 -0.0366153,-0.408674 -0.129925,-1.02287 -0.272843,-1.83667 -0.303553,-1.23429 -0.453558,-1.94179 -0.453558,-2.12723 0,-0.266938 0.509071,-0.465369 1.52721,-0.596475 1.18468,-0.160635 1.9477,-0.377965 2.28905,-0.656714 1.22248,-1.02995 2.47567,-2.33393 3.75957,-3.90957 1.63824,-1.9855 2.45795,-3.47491 2.45795,-4.46707 0,-0.862232 -0.31064,-1.58863 -0.937825,-2.17212 -0.626004,-0.589389 -1.36422,-0.879949 -2.22645,-0.879949 -0.968534,0 -1.92998,0.191345 -2.89143,0.576396 -0.638997,0.242134 -1.31579,0.595294 -2.01739,1.05476 -0.595294,0.379146 -0.917745,0.564585 -0.980346,0.564585 -0.41458,0 -0.620098,-0.484267 -0.620098,-1.45162 0,-0.751205 -0.0307096,-1.29689 -0.0862232,-1.63824 -0.0248039,-0.154729 -0.118114,-0.484267 -0.274024,-0.980346 -0.148824,-0.427573 -0.223235,-0.738212 -0.223235,-0.949636 0,-0.154729 0.106303,-0.303553 0.31064,-0.452376 1.00515,-0.713408 2.35165,-1.27799 4.0395,-1.68785 1.50123,-0.366153 2.95875,-0.545686 4.37967,-0.545686 2.30204,0 4.22612,0.509071 5.77695,1.52603 1.82959,1.18586 2.74851,2.87962 2.74851,5.06945 0,2.92214 -2.21464,6.33445 -6.63919,10.2369 3.13947,-0.160635 5.60333,-0.235047 7.3833,-0.235047 0.360248,0 0.546868,0.223235 0.546868,0.669706z"/></svg>',
    22: '<svg class="captcha-option-22" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><circle class="fil0" cx="25" cy="24.9998" r="23.0008"/><path class="fil1" d="M28.058 29.1399c0,-0.950817 -0.400406,-1.59336 -1.18941,-1.93353 -0.506709,-0.210243 -1.32878,-0.313002 -2.46858,-0.313002 -1.36067,0 -2.10125,0.0484267 -2.21464,0.14528 -0.118114,0.102759 -0.178352,0.751205 -0.178352,1.93943 0,1.24846 0.0708684,1.93471 0.205518,2.06936 0.140556,0.129925 0.902391,0.193707 2.2796,0.193707 1.1398,0 1.94416,-0.0862232 2.40952,-0.2693 0.76656,-0.302372 1.15634,-0.913021 1.15634,-1.83195zm-0.475999 -8.84792c0,-0.908296 -0.453558,-1.50713 -1.36067,-1.80478 -0.50789,-0.15591 -1.34059,-0.237409 -2.50165,-0.237409 -1.1398,0 -1.71265,0.0862232 -1.71265,0.253945 0,0.199613 -0.016536,0.501984 -0.0543324,0.907115 -0.0377965,0.411037 -0.0531513,0.713408 -0.0531513,0.913021 0,1.05358 0.0909477,1.64297 0.2693,1.77171 0.113389,0.0980346 0.784277,0.140556 2.0103,0.140556 2.26897,0 3.40286,-0.647264 3.40286,-1.94416zm6.801 8.90815c0,1.94416 -0.604743,3.55405 -1.81541,4.8285 -1.38193,1.46461 -3.81272,2.19928 -7.28173,2.19928 -0.264575,0 -0.64254,-0.0059057 -1.1398,-0.016536 -0.50789,0 -0.879949,0 -1.12326,0 -3.8954,0 -6.20689,-0.0755929 -6.94746,-0.237409 -0.307096,-0.059057 -0.458282,-0.226779 -0.458282,-0.491354 0,-1.12917 0.0637815,-2.83592 0.193707,-5.12733 0.135831,-2.29023 0.199613,-4.00288 0.199613,-5.14268 0,-1.22012 -0.0637815,-3.52216 -0.187801,-6.89786 -0.0330719,-0.864594 -0.0921289,-2.16621 -0.173628,-3.8954l-0.016536 -0.220873c-0.0106303,-0.199613 0.157092,-0.324813 0.49726,-0.36261 0.346074,-0.042521 1.56619,-0.0637815 3.66271,-0.0637815 3.36507,0 5.33757,0.0106303 5.90452,0.0318908 2.59851,0.0921289 4.51077,0.512615 5.74743,1.26382 1.63115,1.00515 2.45323,2.69536 2.45323,5.08362 0,0.621279 -0.194888,1.28036 -0.572853,1.97723 -0.275206,0.49726 -0.63191,0.988614 -1.07484,1.48587 -0.389776,0.431116 -0.583483,0.63191 -0.583483,0.604743 0,0.0696872 0.13465,0.188982 0.409855,0.346074 0.734669,0.420486 1.31815,1.09019 1.73982,2.00912 0.377965,0.820892 0.566947,1.69612 0.566947,2.62567z"/></svg>',
    23: '<svg class="captcha-option-23" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><circle class="fil0" cx="25" cy="24.9998" r="23.0008"/><path class="fil1" d="M21.1601 14.1501l0 11.8551 -3.4383 0 7.27818 9.8448 7.27818 -9.8448 -3.4383 0 0 -11.8551 -7.67977 0zm0 5.92814m-1.71974 5.92696m1.92053 4.92299m7.27818 0m1.92053 -4.92299m-1.71974 -5.92696m-3.83988 -5.92814"/></svg>',
    24: '<svg class="captcha-option-24" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><circle class="fil0" cx="25" cy="25" r="23.0008"/><path class="fil1" d="M10.7035 24.4708c-1.73273,-0.248039 -1.6217,-1.60871 -0.569309,-2.25834 1.89455,-1.17169 5.54545,-0.65317 7.49079,0.180714 1.09964,0.471275 1.43863,1.07247 2.77804,1.04649 0.440565,-0.00944912 1.05948,-0.0744118 1.50005,-0.16536 1.17996,-3.06033 3.42058,-3.28593 6.32855,-2.98828 0.475999,0.0496079 0.457101,0.034253 0.418123,-0.444108 -0.0259851,-0.303553 -0.050789,-0.607106 -0.0767741,-0.910659 -0.042521,-0.523245 0.0177171,-0.527969 -0.51852,-0.598838 -0.519701,-0.0685061 -0.853964,-0.100397 -0.853964,-0.764197 0,-0.732307 0.550411,-0.492535 1.25437,-0.442927 1.57564,0.109846 1.04413,0.222054 1.86974,1.58155 0.144099,0.23859 0.288198,0.475999 0.433478,0.713408 0.325995,0.537419 0.43584,0.905934 0.268119,0.0496079 -0.152367,-0.772465 -0.304734,-1.54375 -0.457101,-2.31621 -0.284655,-1.45162 2.25361,0.210243 2.59733,0.529151 1.09137,1.01578 1.75399,2.41189 1.69257,3.80681 -0.0555136,1.25319 -0.535056,1.31106 -1.49296,1.96424l0.398044 0.626004c0.617736,-0.287017 1.30634,-0.447652 2.03274,-0.447652 2.66938,0 4.83559,2.16503 4.83559,4.83559 0,2.67056 -2.16621,4.83559 -4.83559,4.83559 -2.67056,0 -4.83559,-2.16503 -4.83559,-4.83559 0,-1.4906 0.675612,-2.82529 1.73628,-3.71232l-0.483086 -0.765378c-3.04616,1.8284 -1.0146,6.49745 -4.55211,7.26991 -1.08192,0.235047 -1.92998,0.340168 -2.77686,0.415761 -1.61816,0.14528 -3.16782,0.510252 -4.72456,-0.0448833l-0.796088 -0.283473 -0.464188 -0.161816c-0.728763,1.33823 -2.14731,2.24535 -3.77728,2.24535 -2.37291,0 -4.29817,-1.92408 -4.29817,-4.29817 0,-2.37291 1.92526,-4.29817 4.29817,-4.29817 2.35637,0 4.26982,1.89691 4.29817,4.2462l0.48663 0.0519701c0,-2.64103 -2.14259,-4.78362 -4.7848,-4.78362 -2.18747,0 -4.03359,1.46934 -4.6029,3.47491l-0.309459 0.566947c-0.170084,0.034253 -0.333081,0.0377965 -0.447652,-0.050789 -0.949636,-0.73585 0.500803,-2.67292 1.37957,-3.48082 0.426391,-0.392138 0.141737,-0.305915 -0.439384,-0.388595zm23.8295 0.819711l0.903572 1.42209c0.116933,-0.0236228 0.236228,-0.0354342 0.360248,-0.0354342 0.988614,0 1.79061,0.801994 1.79061,1.79061 0,0.989795 -0.801994,1.79061 -1.79061,1.79061 -0.988614,0 -1.79179,-0.800813 -1.79179,-1.79061 0,-0.402769 0.133469,-0.774828 0.359066,-1.07484l-0.900028 -1.42445c-0.668525,0.623642 -1.08665,1.51304 -1.08665,2.49929 0,1.88864 1.53076,3.4194 3.4194,3.4194 1.88746,0 3.4194,-1.53076 3.4194,-3.4194 0,-1.88746 -1.53194,-3.4194 -3.4194,-3.4194 -0.446471,0 -0.872862,0.0862232 -1.26382,0.242134zm-16.9942 5.42261l-1.35477 -0.470094c-0.275206,0.263394 -0.648446,0.42521 -1.06066,0.42521 -0.846877,0 -1.5343,-0.687423 -1.5343,-1.53548 0,-0.846877 0.687423,-1.5343 1.5343,-1.5343 0.727582,0 1.33587,0.505528 1.49532,1.1835l1.3843 0.147642c-0.10394,-1.49887 -1.35359,-2.68237 -2.87962,-2.68237 -1.59336,0 -2.88552,1.29217 -2.88552,2.88552 0,1.59454 1.29217,2.88671 2.88552,2.88671 1.01106,0 1.90045,-0.519701 2.41543,-1.30634z"/></svg>',
    31: '<svg class="captcha-option-31" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><polygon class="fil0" points="25,3.1253 32.8676,16.2915 48.0003,19.8361 37.9099,31.3876 39.215,46.8747 25.111,40.8485 10.785,46.8747 12.1587,31.599 1.99967,19.8361 16.9529,16.4214 "/><path class="fil1" d="M32.1116 31.2754c0,1.87329 -0.772465,3.32018 -2.3233,4.33124 -1.31815,0.871681 -2.9623,1.30752 -4.93834,1.30752 -1.52013,0 -2.77095,-0.108665 -3.75602,-0.32127 -2.13786,-0.446471 -3.20679,-0.840971 -3.20679,-1.18232 0,-0.0626004 0.0212605,-0.151186 0.0626004,-0.275206 0.140556,-0.37324 0.347255,-0.934281 0.622461,-1.68667 0.0779552,-0.37324 0.223235,-0.9331 0.42521,-1.67013 0.0885855,-0.253945 0.244496,-0.38387 0.457101,-0.38387 -0.0318908,0 0.420486,0.171265 1.35831,0.503165 0.939006,0.337806 1.70793,0.503165 2.3044,0.503165 1.98668,0 2.97765,-0.6638 2.97765,-1.99258 0,-1.06303 -0.944912,-1.5969 -2.82765,-1.5969 -0.253945,0 -0.585845,0.0106303 -1.00161,0.0307096 -0.41458,0.0212605 -0.689786,0.0307096 -0.819711,0.0307096 -0.622461,0 -0.959085,-0.00472456 -1.02169,-0.0153548 -0.446471,-0.0519701 -0.668525,-0.223235 -0.668525,-0.513796 0,-1.55084 0.0614193,-2.52528 0.180714,-2.91978 0.0838609,-0.255126 0.244496,-0.379146 0.487811,-0.379146 0.347255,0 0.856326,0.0413399 1.53076,0.129925 0.674431,0.0826798 1.1776,0.129925 1.5095,0.129925 0.43584,0 0.79845,-0.14528 1.08901,-0.43584 0.285836,-0.285836 0.431116,-0.654351 0.431116,-1.09964 0,-1.19886 -0.871681,-1.79533 -2.61504,-1.79533 -0.726401,0 -1.71738,0.19725 -2.9623,0.591751 -0.0519701,0.00944912 -0.0980346,0.0153548 -0.13465,0.0153548 -0.13465,0 -0.243315,-0.140556 -0.336625,-0.42521 -0.0212605,-0.426391 -0.0519701,-0.913021 -0.0885855,-1.45871 -0.0106303,-0.119295 -0.0413399,-0.36261 -0.09331,-0.731125 -0.0413399,-0.29056 -0.0626004,-0.529151 -0.0626004,-0.711046 0,-0.5386 0.830341,-0.954361 2.49575,-1.24965 1.14098,-0.201975 2.25125,-0.301191 3.32491,-0.301191 1.7221,0 3.2316,0.379146 4.52849,1.14098 1.5721,0.908296 2.35519,2.17448 2.35519,3.78201 0,1.85203 -0.83979,3.26349 -2.52055,4.22257 0.995701,0.337806 1.7788,0.897666 2.36582,1.69139 0.581121,0.789001 0.8705,1.70202 0.8705,2.73434z"/></svg>',
    32: '<svg class="captcha-option-32" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><polygon class="fil0" points="25,3.1253 32.8676,16.2915 48.0003,19.8361 37.9099,31.3876 39.215,46.8747 25.111,40.8485 10.785,46.8747 12.1587,31.599 1.99967,19.8361 16.9529,16.4214 "/><path class="fil1" d="M32.9715 33.5881c0,0.139374 -0.0897666,0.324813 -0.275206,0.555136 -1.6217,1.93353 -3.78083,2.8997 -6.47264,2.8997 -2.75087,0 -4.98205,-0.939006 -6.69352,-2.8182 -1.66659,-1.82014 -2.50165,-4.11509 -2.50165,-6.88368 0,-2.68355 0.817349,-4.95961 2.44732,-6.82935 1.7032,-1.95597 3.87059,-2.93631 6.49981,-2.93631 2.85481,0 5.09898,0.876406 6.72068,2.63394 0.17599,0.193707 0.262213,0.366153 0.262213,0.514977 0,0.166541 -0.302372,0.790182 -0.916564,1.86502 -0.614193,1.07956 -0.998063,1.68076 -1.15634,1.81541 -0.0732307,0.0685061 -0.162997,0.10394 -0.266938,0.10394 -0.0448833,0 -0.266938,-0.17599 -0.6638,-0.527969 -0.474818,-0.42521 -0.943731,-0.754748 -1.40083,-0.993338 -0.69451,-0.353161 -1.42209,-0.529151 -2.17212,-0.529151 -1.29571,0 -2.33039,0.483086 -3.10758,1.45516 -0.713408,0.897666 -1.07011,2.01384 -1.07011,3.33672 0,1.33705 0.356704,2.46268 1.07011,3.37452 0.77719,0.98507 1.81187,1.48115 3.10758,1.48115 0.767741,0 1.49532,-0.166541 2.18629,-0.505528 0.447652,-0.216149 0.908296,-0.527969 1.37721,-0.926013 0.38387,-0.334262 0.6012,-0.500803 0.646083,-0.500803 0.0909477,0 0.17599,0.0496079 0.266938,0.144099 0.139374,0.158273 0.523245,0.708684 1.15161,1.6536 0.641359,0.979165 0.961448,1.51658 0.961448,1.61698z"/></svg>',
    33: '<svg class="captcha-option-33" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><polygon class="fil0" points="25,3.1253 32.8676,16.2915 48.0003,19.8361 37.9099,31.3876 39.215,46.8747 25.111,40.8485 10.785,46.8747 12.1587,31.599 1.99967,19.8361 16.9529,16.4214 "/><path class="fil1" d="M15.9277 30.5206l9.9133 0 0 2.87489 8.23136 -6.08641 -8.23136 -6.08523 0 2.87489 -9.9133 0 0 6.42186zm4.95724 0m4.95606 1.43745m4.11509 -1.60635m0 -6.08523m-4.11509 -1.60517m-4.95606 1.43745m-4.95724 3.21034"/></svg>',
    34: '<svg class="captcha-option-34" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><polygon class="fil0" points="25,3.1253 32.8676,16.2915 48.0003,19.8361 37.9099,31.3876 39.215,46.8747 25.111,40.8485 10.785,46.8747 12.1587,31.599 1.99967,19.8361 16.9529,16.4214 "/><path class="fil1" d="M25 13.8111l-0.246858 0c-1.78234,0 -2.35874,1.9229 -2.37055,3.35562 -0.0129925,1.51422 0.398044,3.1749 0.357885,4.43045l-2.49811 1.59454c-0.137012,-0.470094 -0.392138,-0.78782 -0.681518,-0.78782l0 0c-0.432297,0 -0.786639,0.708684 -0.786639,1.57328l0 0.151186 -0.566947 0.361429c-0.0649627,-0.734669 -0.388595,-1.29689 -0.773646,-1.29689l0 0c-0.433478,0 -0.786639,0.708684 -0.786639,1.57328l0 0.719314 -2.97411 1.89809 0.0519701 2.09416 9.03926 -3.26703 0.340168 6.00137 -3.56822 2.85127 0.0496079 1.89809 5.41434 -2.09416 5.41434 2.09416 0.0496079 -1.89809 -3.56822 -2.85127 0.340168 -6.00137 9.03926 3.26703 0.0519701 -2.09416 -2.97411 -1.89809 0 -0.719314c0,-0.864594 -0.353161,-1.57328 -0.786639,-1.57328l0 0c-0.385051,0 -0.708684,0.562222 -0.773646,1.29689l-0.566947 -0.361429 0 -0.151186c0,-0.864594 -0.354342,-1.57328 -0.786639,-1.57328l0 0c-0.289379,0 -0.544505,0.317727 -0.680336,0.78782l-2.49811 -1.59454c-0.0413399,-1.25555 0.369697,-2.91623 0.356704,-4.43045 -0.0118114,-1.43272 -0.588208,-3.35562 -2.37055,-3.35562l-0.246858 0z"/></svg>',
    41: '<svg class="captcha-option-41" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><polygon class="fil0" points="25,5.08126 36.5008,25 48.0003,44.9187 25,44.9187 1.99967,44.9187 13.4992,25 "/><path class="fil1" d="M25.2457 27.2678c0,-0.0555136 -0.0354342,-0.0862232 -0.106303,-0.0862232 -0.0874043,0 -0.179533,0.0614193 -0.266938,0.193707 -0.638997,1.02877 -1.27917,2.05755 -1.91817,3.08514 -0.772465,1.19295 -1.52013,2.14377 -2.25125,2.86544 0.552773,0 1.94888,-0.0720495 4.20013,-0.210243 0.0153548,-0.398044 0.0874043,-1.38548 0.210243,-2.95167 0.0862232,-1.24256 0.132288,-2.20519 0.132288,-2.89615zm7.40338 9.4751c0,0.148824 -0.122839,0.251583 -0.37324,0.297647 -0.179533,0.0307096 -0.429935,0.0354342 -0.74648,0.0153548 -0.450014,-0.0307096 -0.644902,-0.0413399 -0.572853,-0.0413399 -0.389776,0 -0.583483,0.194888 -0.583483,0.583483 0,0.239771 0.0153548,0.598838 0.0460644,1.08429 0.0307096,0.48663 0.0401587,0.849239 0.0401587,1.09019 0,0.347255 -0.153548,0.522064 -0.460644,0.522064 -3.44775,0 -5.26434,-0.0413399 -5.44269,-0.128744 -0.179533,-0.0814986 -0.271662,-0.188982 -0.271662,-0.322451 0,-0.147642 0.0661438,-0.516158 0.188982,-1.10909 0.122839,-0.589389 0.190163,-1.01814 0.190163,-1.28508 0,-0.3319 -0.184258,-0.496079 -0.557498,-0.496079 -0.670887,0 -1.66895,0.0200794 -3.00364,0.0614193 -1.33587,0.0354342 -2.33866,0.0566947 -3.00364,0.0566947 -0.803175,0 -1.2024,-0.311821 -1.2024,-0.941368 0,-0.322451 -0.00472456,-0.79845 -0.0153548,-1.43272 -0.00944912,-0.634272 -0.0153548,-1.11027 -0.0153548,-1.43272 0,-0.296466 0.158273,-0.614193 0.465369,-0.941368 1.45871,-1.56029 2.52291,-2.80875 3.19262,-3.75012 0.322451,-0.450014 1.40674,-2.20519 3.25404,-5.25961 0.240952,-0.460644 0.629547,-1.09019 1.16697,-1.88746 0.142918,-0.174809 0.291741,-0.256307 0.450014,-0.256307 0.240952,0 0.982708,0.179533 2.22527,0.537419 1.24374,0.36261 2.09298,0.542143 2.54299,0.542143 0.317727,0 0.480724,0.204337 0.480724,0.614193 0,0.388595 -0.0460644,0.976802 -0.138193,1.7599 -0.0862232,0.783096 -0.132288,1.37603 -0.132288,1.77525l0 6.31319c0.188982,0 0.516158,-0.0307096 0.987433,-0.0921289 0.419305,-0.0614193 0.74648,-0.0862232 0.976802,-0.0862232 0.188982,0 0.281111,0.112208 0.281111,0.34253 0,0.209062 -0.00944912,0.522064 -0.0354342,0.946093 -0.0259851,0.419305 -0.0354342,0.737031 -0.0354342,0.956723 0,0.219692 0.0153548,0.548049 0.050789,0.982708 0.0354342,0.434659 0.050789,0.761835 0.050789,0.981527z"/></svg>',
    42: '<svg class="captcha-option-42" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><polygon class="fil0" points="25,5.08126 36.5008,25 48.0003,44.9187 25,44.9187 1.99967,44.9187 13.4992,25 "/><path class="fil1" d="M30.2986 31.4561c0,-1.47052 -0.440565,-2.67292 -1.31815,-3.60366 -0.887036,-0.966172 -2.06227,-1.44808 -3.52334,-1.44808 -1.34059,0 -2.00912,0.178352 -2.00912,0.535056 0,0.511433 -0.00944912,1.28744 -0.0271662,2.31621 -0.0177171,1.0335 -0.0259851,1.8036 -0.0259851,2.31621 0,0.503165 0.00826798,1.265 0.0259851,2.27606 0.0177171,1.01578 0.0271662,1.77762 0.0271662,2.29377 0,0.374421 0.69451,0.562222 2.08471,0.562222 1.50595,0 2.69064,-0.504347 3.55051,-1.50123 0.810262,-0.949636 1.21539,-2.20046 1.21539,-3.74657zm4.99858 0c0,2.55717 -0.824435,4.77535 -2.46858,6.65454 -1.45162,1.67958 -3.49145,2.56189 -6.11948,2.65048 -0.504347,0.0177171 -1.89337,0.0271662 -4.16588,0.0271662 -0.422848,0 -1.06421,-0.0129925 -1.92408,-0.0401587 -0.855145,-0.0271662 -1.4965,-0.0401587 -1.92408,-0.0401587 -0.24922,0 -0.379146,-0.0980346 -0.379146,-0.298828 0,-0.956723 0.0401587,-2.39653 0.111027,-4.31588 0.0767741,-1.91581 0.112208,-3.35444 0.112208,-4.31234 0,-1.00161 -0.0354342,-2.49811 -0.112208,-4.49424 -0.0708684,-1.99613 -0.111027,-3.49263 -0.111027,-4.48597 0,-0.183077 0.129925,-0.289379 0.379146,-0.324813 0.618917,-0.067325 1.62997,-0.102759 3.04262,-0.102759 2.67646,0 4.41392,0.0401587 5.20646,0.115752 2.06227,0.209062 3.67571,0.731125 4.84267,1.56855 1.0961,0.779552 1.95951,1.87919 2.59733,3.28711 0.605925,1.33233 0.913021,2.6989 0.913021,4.11155z"/></svg>',
    43: '<svg class="captcha-option-43" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><polygon class="fil0" points="25,5.08126 36.5008,25 48.0003,44.9187 25,44.9187 1.99967,44.9187 13.4992,25 "/><path class="fil1" d="M33.9471 34.8058l-9.77629 0 0 2.83592 -8.11797 -6.00255 8.11797 -6.00137 0 2.83592 9.77629 0 0 6.33209zm-4.88874 0m-4.88756 1.41855m-4.0584 -1.58391m0 -6.00137m4.0584 -1.58391m4.88756 1.41855m4.88874 3.16545"/></svg>',
    44: '<svg class="captcha-option-44" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><polygon class="fil0" points="25,5.08126 36.5008,25 48.0003,44.9187 25,44.9187 1.99967,44.9187 13.4992,25 "/><path class="fil1" d="M15.7092 35.309c-1.29925,0.248039 -2.2229,0.0614193 -2.46976,-0.901209 -0.298828,-1.1587 -0.210243,-2.35755 0.160635,-3.52452 2.82292,-8.88808 14.3839,-10.8559 19.2455,-2.72725 4.2332,1.32642 6.3439,3.27412 6.33091,5.84192 -0.00708684,1.41737 -0.168903,1.31106 -1.43981,1.31106l-0.894123 0c0,-2.03274 -1.64887,-3.68161 -3.68161,-3.68161 -2.03274,0 -3.68161,1.64887 -3.68161,3.68161l-6.15137 0c0,-2.03274 -1.64887,-3.68161 -3.68161,-3.68161 -2.03274,0 -3.68161,1.64887 -3.68161,3.68161l-0.0555136 0zm3.73713 3.20561c1.77053,0 3.20561,-1.43508 3.20561,-3.20561 0,-1.76935 -1.43508,-3.20561 -3.20561,-3.20561 -1.76935,0 -3.20561,1.43627 -3.20561,3.20561 0,1.77053 1.43627,3.20561 3.20561,3.20561zm0 -1.83785c0.755929,0 1.36776,-0.61183 1.36776,-1.36776 0,-0.754748 -0.61183,-1.36658 -1.36776,-1.36658 -0.754748,0 -1.36658,0.61183 -1.36658,1.36658 0,0.755929 0.61183,1.36776 1.36658,1.36776zm13.5146 1.78825c1.74218,0 3.156,-1.41264 3.156,-3.156 0,-1.74218 -1.41382,-3.15482 -3.156,-3.15482 -1.74218,0 -3.156,1.41264 -3.156,3.15482 0,1.74336 1.41382,3.156 3.156,3.156zm0 -1.84022c0.726401,0 1.31461,-0.589389 1.31461,-1.31579 0,-0.72522 -0.588208,-1.31461 -1.31461,-1.31461 -0.726401,0 -1.31461,0.589389 -1.31461,1.31461 0,0.726401 0.588208,1.31579 1.31461,1.31579zm-9.56014 -11.5716c0.016536,1.62761 0.531513,4.00052 -1.35713,4.01351 -1.76698,0.0129925 -3.16427,-0.0885855 -4.93126,-0.0755929 -1.12444,0.00826798 -1.09492,0.0401587 -0.520883,-1.00515 0.583483,-1.06066 1.42682,-1.95597 2.57961,-2.65284 1.10909,-0.672068 4.20604,-2.51346 4.22966,-0.27993zm2.02093 4.00879l5.42379 -0.0814986c0.594113,-0.00944912 1.28626,0.184258 0.615374,-0.88113 -1.22839,-1.9536 -3.0934,-3.34262 -5.8053,-3.9769 -0.935463,-0.219692 -1.16578,0.336625 -1.20949,1.02405 -0.0614193,0.987433 -0.441746,3.93674 0.975621,3.91548z"/></svg>'
}

grafical_forms = {
    11: ['blue', 'black', 'square', 'number', 'number one'],
    12: ['yellow', 'white', 'square', 'letter', 'letter a'],
    13: ['red', 'white', 'square', 'arrow', 'arrow up'],
    14: ['pink', 'green', 'square', 'mean of transport', 'ship'],
    21: ['pink', 'grey', 'circle', 'number', 'number two'],
    22: ['blue', 'black', 'circle', 'letter', 'letter b'],
    23: ['yellow', 'green', 'circle', 'arrow', 'arrow down'],
    24: ['red', 'black', 'circle', 'mean of transport', 'motorcycle'],
    31: ['red', 'black', 'star', 'number', 'number three'],
    32: ['pink', 'green', 'star', 'letter', 'letter c'],
    33: ['blue', 'grey', 'star', 'arrow', 'arrow right'],
    34: ['yellow', 'grey', 'star', 'mean of transport', 'airplane'],
    41: ['yellow', 'green', 'triangle', 'number', 'number four'],
    42: ['red', 'grey', 'triangle', 'letter', 'letter d'],
    43: ['pink', 'white', 'triangle', 'arrow', 'arrow left'],
    44: ['blue', 'white', 'triangle', 'mean of transport', 'car'],
}


class Captcha(object):
    attributes = attributes
    grafical_forms = grafical_forms
    svg_forms = svg_forms

    def __init__(self, _id, token="", num_opt=4):
        super(Captcha, self).__init__()
        self._id = _id
        self.token = token
        self.keys_attributes = [x for x in attributes]
        self.keys_lines_cols = [y for y in grafical_forms]
        self.num_opt = num_opt
        self._choicer()

    @property
    def choice(self):
        return self._choice

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    def _choicer(self):
        count_attr = len(self.keys_attributes)
        choice = self.keys_attributes[random.randint(0, count_attr - 1)]
        self._choice = choice

    @staticmethod
    def check(attribute, number):
        try:
            number = int(number)
        except ValueError:
            return False
        if attribute in grafical_forms[number]:
            return True
        else:
            return False

    @property
    def html(self):
        num_opt = self.num_opt
        choice = self.choice
        options = []
        random.shuffle(self.keys_lines_cols)
        cont_err = 0
        cont_ok = 0
        for x in self.keys_lines_cols:
            t_choice = grafical_forms[x]
            if choice in t_choice:
                if cont_ok == 0:
                    options.append(x)
                    cont_ok += 1
            else:
                if cont_err < num_opt - 1:
                    options.append(x)
                    cont_err += 1
                else:
                    if cont_ok == 1:
                        break
        random.shuffle(options)
        question = "Qual figura abaixo possui %s?" % attributes[choice]
        content = []
        if self.token:
            token = self.token
        else:
            token = choice
        for x in options:
            content.append(
                DIV(
                    DIV(
                        DIV(
                            XML(svg_forms[x]),
                            _class='captcha-option-svg'),
                        _class='captcha-option link', _cmd_option=str(x), _token=token, _id_captcha=self._id),
                    _class='captcha-option-container')
            )
        html = DIV(
            DIV(
                question,
                _class='captcha-question-container'),
            DIV(
                *content,
                _class='captcha-options-container'),
            _class='captcha-container')
        self._html = html
        return self._html

    @property
    def html_ok(self):
        self._html_ok = DIV(
            DIV(
                XML('<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50px" height="50px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" viewBox="0 0 50 50" xmlns:xlink="http://www.w3.org/1999/xlink"><circle class="fil0" cx="25.1541" cy="25.1175" r="24.5529"/><polygon class="fil1" points="14.6544,18.9408 20.4585,26.0181 39.3804,13.6859 43.962,20.7361 21.8877,35.1224 18.7388,37.1752 16.3517,34.266 8.16404,24.2795 "/></svg>'),
                _class="captcha-ok-svg-container", _id="captcha-ok-svg-container-%s" % (self._id)),
            _class='captcha-container')
        return self._html_ok


if __name__ == '__main__':
    captcha = Captcha("teste")
    captcha.token = '----------------------------------------------'
    print(captcha.choice)
    print(captcha.html)
