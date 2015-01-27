from models.gamelogmodel import GamelogModel
from models.paymentmodel import PaymentModel
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
]

all_spout_models = [GamelogModel, PaymentModel,]
