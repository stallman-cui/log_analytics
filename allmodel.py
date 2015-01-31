from spouts.gamelogspout import GamelogSpout
from spouts.paymentspout import PaymentSpout
#from models.syncuserspout import SyncUserSpout

from models.signuphourmodel import SignupHourModel
from models.loginhourmodel import LoginHourModel
from models.createrolehourmodel import CreateroleHourModel
from models.signupdaymodel import SignupDayModel
from models.logindaymodel import LoginDayModel
from models.createroledaymodel import CreateroleDayModel
from models.paysummarymodel import PaySummaryModel
from models.servermodel import ServerModel
from models.coinfiltermodel import CoinFilterModel
from models.cointypemodel import CoinTypeModel
from models.coinhourmodel import CoinHourModel
from models.coindaymodel import CoinDayModel
from models.payorderdetailmodel import PayorderDetailModel
from models.userlogininfomodel import UserLoginInfoModel
from models.mainlinemodel import MainlineModel
from models.payretentiontracemodel import PayRetentionTraceModel
from models.paytracedaymodel import PayTraceDayModel
from models.loginretentionmodel import LoginRetentionModel
from models.gamecopymodel import GameCopyModel
from models.shopmodel import ShopModel
from models.shopfiltermodel import ShopFilterModel
from models.userpayfiltermodel import UserPayFilterModel
from models.userpaymodel import UserPayModel

from models.combatmodel import CombatModel
from models.usercentermodel import UserCenterModel
from models.userlevelmodel import UserLevelModel
from models.activedaymodel import ActiveDayModel
from models.serverstarttimemodel import ServerStartTimeModel
from models.activeweekmodel import ActiveWeekModel
from models.activemonthmodel import ActiveMonthModel

all_bolt_models = [LoginHourModel, SignupHourModel, 
                   CreateroleHourModel, 
                   LoginDayModel, SignupDayModel, 
                   CreateroleDayModel, 
                   PaySummaryModel, ServerModel,

                   PayorderDetailModel, UserLoginInfoModel,
                   CoinFilterModel, CoinTypeModel,
                   CoinHourModel, CoinDayModel,
                   MainlineModel, 
                   PayRetentionTraceModel,
                   PayTraceDayModel,
                   LoginRetentionModel,
                   GameCopyModel,
                   ShopFilterModel, ShopModel,
                   UserPayFilterModel, UserPayModel,
]

bolt_sync_models = [UserCenterModel, UserLevelModel, CombatModel, ]

bolt_timer_models = [ServerStartTimeModel, ActiveDayModel,
                      ActiveWeekModel,
                      ActiveMonthModel,
]

all_spouts =  [GamelogSpout, PaymentSpout, ]#SyncUserSpout]

