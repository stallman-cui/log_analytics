from spouts.gamelogspout import GamelogSpout
from spouts.paymentspout import PaymentSpout
from spouts.syncuserspout import SyncUserSpout

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

from models.usercentermodel import UserCenterModel
from models.userlevelmodel import UserLevelModel
from models.activedaymodel import ActiveDayModel
from models.serverstarttimemodel import ServerStartTimeModel
from models.activeweekmodel import ActiveWeekModel
from models.activemonthmodel import ActiveMonthModel

bolt_models_1 = [LoginHourModel, SignupHourModel, 
                 CreateroleHourModel, 
                 LoginDayModel, SignupDayModel, 
                 CreateroleDayModel, 
                 PaySummaryModel, ServerModel,
                 CoinFilterModel, CoinTypeModel,
                 CoinHourModel, CoinDayModel,
                 PayRetentionTraceModel,
                 PayTraceDayModel,
                 LoginRetentionModel,
                 UserLoginInfoModel,
]

bolt_models_2 = [PayorderDetailModel, 
                 MainlineModel, 
                 GameCopyModel,
                 ShopFilterModel, ShopModel,
                 UserPayFilterModel, UserPayModel,
                 UserCenterModel,
]

bolt_timer_models = [ServerStartTimeModel, ActiveDayModel,
                     ActiveWeekModel,
                     ActiveMonthModel,
                     UserLevelModel,
]

all_spouts =  [GamelogSpout, PaymentSpout, SyncUserSpout]
