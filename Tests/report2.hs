import System.IO
import System.Exit
import Data.List.Split
import Data.Char

main = do
	putStrLn "Customer         Order#         Date         Items"
	contents <- readFile "CustDBSalesDB.join"
	let databaseJoine1 = lines contents
	contents <- readFile "OrderDBSalesDB.join"
	let databaseJoine2 = lines contents
	putStrLn $ printReport databaseJoine1 databaseJoine2 0 1 2 3 1
	exitSuccess

printReport :: [String] -> [String] -> Int -> Int -> Int -> Int -> Int -> String
printReport database1 database2 n namePos orderPos datePos itemPos
	| length database1 == n || length database2 == n = ""
	| otherwise = do
		((splitOn "|" $ database1 !! n) !! namePos) ++ "   " ++ ((splitOn "|" $ database2 !! n) !! orderPos) ++ "   " ++ ((splitOn "|" $ database2 !! n) !! datePos) ++ "   " ++ ((splitOn "|" $ database2 !! n) !! itemPos) ++ "\n" ++ printReport database1 database2 (n+1) namePos orderPos datePos itemPos